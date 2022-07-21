
# Based on https://github.com/lefticus/cpp_starter_project

function(enable_sanitisers project_name)

    if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU" OR CMAKE_CXX_COMPILER_ID MATCHES ".*Clang")

        option(ENABLE_COVERAGE "Enable coverage reporting for gcc/clang" FALSE)
        if (ENABLE_COVERAGE)
            target_compile_options(${project_name} INTERFACE --coverage -O0 -g)
            target_link_libraries(${project_name} INTERFACE --coverage)
        endif ()

        set(SANITISERS "")
        set(ADDITIONAL_COMPILE_OPTIONS "")

        option(ENABLE_SANITISER_ADDRESS "Enable address sanitiser" FALSE)
        if (ENABLE_SANITISER_ADDRESS)
            list(APPEND SANITISERS "address")
            list(APPEND ADDITIONAL_COMPILE_OPTIONS "-O1" "-g" "-fno-omit-frame-pointer" "-fno-optimize-sibling-calls" "-static-libasan")
        endif ()

        option(ENABLE_SANITISER_LEAK "Enable leak sanitiser" FALSE)
        if (ENABLE_SANITISER_LEAK)
            list(APPEND SANITISERS "leak")
            list(APPEND ADDITIONAL_COMPILE_OPTIONS "-O1" "-g" "-fno-omit-frame-pointer" "-fno-optimize-sibling-calls")
        endif ()

        option(ENABLE_SANITISER_UNDEFINED_BEHAVIOUR "Enable undefined behavior sanitiser" FALSE)
        if (ENABLE_SANITISER_UNDEFINED_BEHAVIOUR)
            list(APPEND SANITISERS "undefined")
        endif ()

        option(ENABLE_SANITISER_THREAD "Enable thread sanitiser" FALSE)
        if (ENABLE_SANITISER_THREAD)
            if ("address" IN_LIST SANITISERS OR "leak" IN_LIST SANITISERS)
                message(WARNING "Thread sanitiser does not work with Address and Leak sanitiser enabled")
            else ()
                list(APPEND SANITISERS "thread")
                list(APPEND ADDITIONAL_COMPILE_OPTIONS "-O1" "-g")
            endif ()
        endif ()

        option(ENABLE_SANITISER_MEMORY "Enable memory sanitiser" FALSE)
        if (ENABLE_SANITISER_MEMORY AND CMAKE_CXX_COMPILER_ID MATCHES ".*Clang")
            if ("address" IN_LIST SANITISERS
                    OR "thread" IN_LIST SANITISERS
                    OR "leak" IN_LIST SANITISERS)
                message(WARNING "Memory sanitiser does not work with Address, Thread and Leak sanitiser enabled")
            else ()
                list(APPEND SANITISERS "memory")
                list(APPEND ADDITIONAL_COMPILE_OPTIONS "-O1" "-g" "-fno-omit-frame-pointer" "-fno-optimize-sibling-calls")
            endif ()
        endif ()

        list(JOIN SANITISERS "," LIST_OF_SANITISERS)
        list(JOIN ADDITIONAL_COMPILE_OPTIONS " " LIST_OF_ADDITIONAL_COMPILE_OPTIONS)

    endif ()

    if (LIST_OF_SANITISERS)
        if (NOT "${LIST_OF_SANITISERS}" STREQUAL "")
            target_compile_options(${project_name} INTERFACE -fsanitize=${LIST_OF_SANITISERS})
            target_compile_options(${project_name} INTERFACE ${ADDITIONAL_COMPILE_OPTIONS})
            target_link_libraries(${project_name} INTERFACE -fsanitize=${LIST_OF_SANITISERS})
        endif ()
    endif ()

endfunction()

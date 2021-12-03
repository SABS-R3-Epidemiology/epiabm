


set(
    epiabm_src
    dataclasses/population.cpp
    dataclasses/cell.cpp
    dataclasses/microcell.cpp
    dataclasses/person.cpp
    dataclasses/place.cpp
    population_factory.cpp
    covidsim.cpp
)

set(
    epiabm_hdr
    dataclasses/population.hpp
    dataclasses/cell.hpp
    dataclasses/microcell.hpp
    dataclasses/person.hpp
    dataclasses/place.hpp
    dataclasses/infection_status.hpp
    population_factory.hpp
    covidsim.hpp
)

add_library(epiabm_lib STATIC ${epiabm_src} ${epiabm_hdr})

target_include_directories(
        epiabm_lib INTERFACE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)

target_link_libraries(epiabm_lib PRIVATE project_warnings project_settings)

if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    if (CMAKE_CXX_COMPILER_VERSION VERSION_LESS 8.4)
        target_link_libraries(epiabm_lib PRIVATE stdc++fs)
    endif ()
endif ()

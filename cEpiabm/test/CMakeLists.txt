
#find_package(Catch2 CONFIG REQUIRED)
#message(STATUS "Found Catch2 ${Catch2_VERSION}")

set(CATCH_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/catch)
add_library(catch INTERFACE)
target_include_directories(catch INTERFACE ${CATCH_INCLUDE_DIR})

add_library(catch_main STATIC catch_main.cpp)
#target_link_libraries(catch_main PUBLIC Catch2::Catch2WithMain)
target_link_libraries(catch_main PRIVATE project_settings)
target_link_libraries(catch_main PUBLIC catch)

add_definitions(-DEPIABM_TEST_DIR=\"${CMAKE_CURRENT_LIST_DIR}\")

set(
    test_src
    test_population_factory.cpp
    dataclasses/test_person.cpp
    dataclasses/test_microcell.cpp
    dataclasses/test_cell.cpp
    dataclasses/test_population.cpp
    dataclasses/test_household.cpp
    dataclasses/test_place.cpp
)

add_executable(unit_tests ${test_src})
target_link_libraries(unit_tests PRIVATE epiabm_lib project_warnings project_settings)
target_link_libraries(unit_tests PUBLIC catch_main)

# automatically discover tests related to the "tests"
#include(Catch)
enable_testing()
#include(CTest)
include(../cmake/Catch.cmake)
#set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/../cmake)
catch_discover_tests(unit_tests)
#add_test(unit_tests, unit_tests)


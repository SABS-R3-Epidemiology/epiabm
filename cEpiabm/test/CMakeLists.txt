
find_package(Catch2 CONFIG REQUIRED)
message(STATUS "Found Catch2 ${Catch2_VERSION}")

add_library(catch STATIC catch_main.cpp)
target_link_libraries(catch PUBLIC Catch2::Catch2WithMain)
#target_link_libraries(catch_main PUBLIC Catch2::Catch2WithMain)
target_link_libraries(catch PRIVATE project_settings)

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
target_link_libraries(unit_tests PRIVATE epiabm_lib project_warnings project_settings catch)

# automatically discover tests related to the "tests"
include(Catch)
catch_discover_tests(unit_tests)

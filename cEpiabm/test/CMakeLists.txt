
#find_package(Catch2 CONFIG REQUIRED)
#message(STATUS "Found Catch2 ${Catch2_VERSION}")

set(src_testdata_path ${CMAKE_CURRENT_SOURCE_DIR}/testdata)
set(build_testdata_path ${PROJECT_BINARY_DIR}/testdata)

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
    dataclasses/test_person.cpp
    dataclasses/test_microcell.cpp
    dataclasses/test_cell.cpp
    dataclasses/test_population.cpp
    dataclasses/test_household.cpp
    dataclasses/test_place.cpp
    dataclasses/test_compartment_counter.cpp
    dataclasses/test_infection_status.cpp
    test_population_factory.cpp
    test_toy_population_factory.cpp
    test_output_file_handler.cpp
    test_log_file.cpp
    test_covidsim.cpp
    configuration/test_json_factory.cpp
    configuration/test_simulation_config.cpp
    configuration/test_infection_config.cpp
    configuration/test_population_config.cpp
    configuration/test_host_progression_config.cpp
    sweeps/test_household_sweep.cpp
    sweeps/test_new_infection_sweep.cpp
    sweeps/test_basic_host_progression_sweep.cpp
    sweeps/test_random_seed_sweep.cpp
    sweeps/test_spatial_sweep.cpp
    sweeps/test_place_sweep.cpp
    reporters/test_cell_compartment_reporter.cpp
    reporters/test_percell_compartment_reporter.cpp
    reporters/test_population_compartment_reporter.cpp
    utilities/test_inverse_cdf.cpp
    utilities/test_random_manager.cpp
    utilities/test_random_generator.cpp
    utilities/test_distance_metrics.cpp
    test_basic_simulation.cpp
)

add_executable(unit_tests ${test_src})
target_link_libraries(unit_tests PRIVATE epiabm_lib project_warnings project_settings)
target_link_libraries(unit_tests PUBLIC catch_main)

function (setup_testdata)
    if(EXISTS "${build_testdata_path}")
        file(REMOVE_RECURSE "${build_testdata_path}")
        file(MAKE_DIRECTORY "${build_testdata_path}")
    endif()
    file(GLOB src_testdata_files "${src_testdata_path}/*")
    file(COPY ${src_testdata_files} DESTINATION "${build_testdata_path}")
endfunction()

# automatically discover tests related to the "tests"
#include(Catch)
enable_testing()
#include(CTest)
include(../cmake/Catch.cmake)
#set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/../cmake)
catch_discover_tests(unit_tests)
#add_test(unit_tests, unit_tests)


setup_testdata()

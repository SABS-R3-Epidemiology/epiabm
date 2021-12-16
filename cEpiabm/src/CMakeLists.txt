


set(
    epiabm_src
    dataclasses/population.cpp
    dataclasses/compartment_counter.cpp
    dataclasses/cell.cpp
    dataclasses/microcell.cpp
    dataclasses/person.cpp
    dataclasses/membersInterface.cpp
    dataclasses/place.cpp
    dataclasses/household.cpp
    population_factory.cpp
    household_linker.cpp
    output_folder_handler.cpp
    logfile.cpp
    covidsim.cpp
    sweeps/sweep_interface.cpp
    sweeps/household_sweep.cpp
    sweeps/new_infection_sweep.cpp
    sweeps/basic_host_progression_sweep.cpp
    sweeps/random_seed_sweep.cpp
    reporters/timestep_reporter_interface.cpp
    reporters/cell_compartment_reporter.cpp
    reporters/percell_compartment_reporter.cpp
    reporters/population_compartment_reporter.cpp
    simulations/basic_simulation.cpp
)

set(
    epiabm_hdr
    dataclasses/population.hpp
    dataclasses/compartment_counter.hpp
    dataclasses/cell.hpp
    dataclasses/microcell.hpp
    dataclasses/infection_status.hpp
    dataclasses/person.hpp
    dataclasses/membersInterface.hpp
    dataclasses/place.hpp
    dataclasses/household.hpp
    population_factory.hpp
    household_linker.hpp
    output_folder_handler.hpp
    logfile.hpp
    covidsim.hpp
    sweeps/sweep_interface.hpp
    sweeps/household_sweep.hpp
    sweeps/new_infection_sweep.hpp
    sweeps/basic_host_progression_sweep.hpp
    sweeps/random_seed_sweep.hpp
    reporters/timestep_reporter_interface.hpp
    reporters/cell_compartment_reporter.hpp
    reporters/percell_compartment_reporter.hpp
    reporters/population_compartment_reporter.hpp
    simulations/basic_simulation.hpp
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




set(
    epiabm_src
    dataclasses/population.cpp
    dataclasses/cell.cpp
    dataclasses/microcell.cpp
    dataclasses/person.cpp
    dataclasses/membersInterface.cpp
    dataclasses/place.cpp
    dataclasses/household.cpp
    population_factory.cpp
    output_folder_handler.cpp
    logfile.cpp
    covidsim.cpp
    sweeps/sweep_interface.cpp
    sweeps/household_sweep.cpp
    sweeps/new_infection_sweep.cpp
)

set(
    epiabm_hdr
    dataclasses/population.hpp
    dataclasses/cell.hpp
    dataclasses/microcell.hpp
    dataclasses/person.hpp
    dataclasses/membersInterface.hpp
    dataclasses/place.hpp
    dataclasses/household.hpp
    population_factory.hpp
    output_folder_handler.hpp
    logfile.hpp
    covidsim.hpp
    sweeps/sweep_interface.hpp
    sweeps/household_sweep.hpp
    sweeps/new_infection_sweep.hpp
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

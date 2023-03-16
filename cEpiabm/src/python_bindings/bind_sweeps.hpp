#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "sweeps/sweep_interface.hpp"
#include "sweeps/household_sweep.hpp"
#include "sweeps/basic_host_progression_sweep.hpp"
#include "sweeps/host_progression_sweep.hpp"
#include "sweeps/new_infection_sweep.hpp"
#include "sweeps/random_seed_sweep.hpp"
#include "sweeps/spatial_sweep.hpp"
#include "sweeps/place_sweep.hpp"


namespace py = pybind11;

void bind_sweeps(py::module &m)
{
    using namespace epiabm;

    py::class_<SweepInterface, SweepInterfacePtr>(m, "SweepInterface")
        .def("bind_population", &SweepInterface::bind_population)
        .def("__call__", &SweepInterface::operator());

    py::class_<HouseholdSweep, HouseholdSweepPtr>(m, "HouseholdSweep",
        py::base<SweepInterface>())
        .def(py::init<SimulationConfigPtr>());
        
    py::class_<BasicHostProgressionSweep, BasicHostProgressionSweepPtr>(m, "BasicHostProgressionSweep",
        py::base<SweepInterface>())
        .def(py::init<SimulationConfigPtr>());

    py::class_<HostProgressionSweep, HostProgressionSweepPtr>(m, "HostProgressionSweep",
        py::base<SweepInterface>())
        .def(py::init<SimulationConfigPtr>());
    
    py::class_<NewInfectionSweep, NewInfectionSweepPtr>(m, "NewInfectionSweep",
        py::base<SweepInterface>())
        .def(py::init<SimulationConfigPtr>());

    py::class_<RandomSeedSweep, RandomSeedSweepPtr>(m, "RandomSeedSweep",
        py::base<SweepInterface>())
        .def(py::init<SimulationConfigPtr, int>());
    
    py::class_<SpatialSweep, SpatialSweepPtr>(m, "SpatialSweep",
        py::base<SweepInterface>())
        .def(py::init<SimulationConfigPtr>());
        
    py::class_<PlaceSweep, PlaceSweepPtr>(m, "PlaceSweep",
        py::base<SweepInterface>())
        .def(py::init<SimulationConfigPtr>());
}


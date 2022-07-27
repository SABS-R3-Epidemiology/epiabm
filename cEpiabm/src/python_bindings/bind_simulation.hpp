#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "simulations/basic_simulation.hpp"
#include "simulations/threaded_simulation.hpp"


namespace py = pybind11;

void bind_simulation(py::module &m)
{
    using namespace epiabm;

    py::class_<BasicSimulation, BasicSimulationPtr>(m, "BasicSimulation")
        .def(py::init<PopulationPtr>())
        .def("add_sweep", &BasicSimulation::addSweep)
        .def("add_timestep_reporter", &BasicSimulation::addTimestepReporter)
        .def("simulate", &BasicSimulation::simulate);

    py::class_<ThreadedSimulation, ThreadedSimulationPtr>(m, "ThreadedSimulation")
        .def(py::init<PopulationPtr, std::optional<size_t>>())
        .def("add_sweep", &ThreadedSimulation::addSweep)
        .def("add_timestep_reporter", &ThreadedSimulation::addTimestepReporter)
        .def("simulate", &ThreadedSimulation::simulate);
}


#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "reporters/timestep_reporter_interface.hpp"
#include "reporters/cell_compartment_reporter.hpp"
#include "reporters/percell_compartment_reporter.hpp"
#include "reporters/population_compartment_reporter.hpp"


namespace py = pybind11;

void bind_reporters(py::module &m)
{
    using namespace epiabm;

    py::class_<TimestepReporterInterface, TimestepReporterInterfacePtr>(m, "TimestepReporterInterface")
        .def(py::init<const std::string, bool>());

    py::class_<CellCompartmentReporter, CellCompartmentReporterPtr>(m, "CellCompartmentReporter",
        py::base<TimestepReporterInterface>())
        .def(py::init<const std::string>())
        .def("compartments", &CellCompartmentReporter::compartments,
            py::return_value_policy::reference);
    
    py::class_<PerCellCompartmentReporter, PerCellCompartmentReporterPtr>(m, "PerCellCompartmentReporter",
        py::base<TimestepReporterInterface>())
        .def(py::init<const std::string>())
        .def("compartments", &PerCellCompartmentReporter::compartments,
            py::return_value_policy::reference);

    py::class_<PopulationCompartmentReporter, PopulationCompartmentReporterPtr>(m, "PopulationCompartmentReporter",
        py::base<TimestepReporterInterface>())
        .def(py::init<const std::string>())
        .def("compartments", &PopulationCompartmentReporter::compartments,
            py::return_value_policy::reference);
}


#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "dataclasses/infection_status.hpp"
#include "dataclasses/compartment_counter.hpp"
#include "population_factory.hpp"
#include "toy_population_factory.hpp"
#include "household_linker.hpp"

namespace py = pybind11;

void bind_dataclasses(py::module &m)
{
    using namespace epiabm;

    py::enum_<InfectionStatus>(m, "InfectionStatus")
        .value("Susceptible", InfectionStatus::Susceptible)
        .value("Exposed", InfectionStatus::Exposed)
        .value("InfectASympt", InfectionStatus::InfectASympt)
        .value("InfectMild", InfectionStatus::InfectMild)
        .value("InfectGP", InfectionStatus::InfectGP)
        .value("InfectHosp", InfectionStatus::InfectHosp)
        .value("InfectICU", InfectionStatus::InfectICU)
        .value("InfectICURecov", InfectionStatus::InfectICURecov)
        .value("Recovered", InfectionStatus::Recovered)
        .value("Dead", InfectionStatus::Dead)
        .export_values();


    py::class_<PersonParams>(m, "PersonParams")
        .def_readwrite("age", &PersonParams::age)
        .def_readwrite("susceptibility", &PersonParams::susceptibility)
        .def_readwrite("infectiousness", &PersonParams::infectiousness)
        .def_readonly("next_status_time", &PersonParams::next_status_time);
    py::class_<Person, PersonPtr>(m, "Person")
        .def("status", &Person::status, py::return_value_policy::copy)
        .def("params", &Person::params, py::return_value_policy::reference)
        .def("cell_pos", &Person::cellPos, py::return_value_policy::copy)
        .def("microcell_pos", &Person::microcellPos, py::return_value_policy::copy)
        .def("microcell", &Person::microcell, py::return_value_policy::copy)
        .def("places", &Person::places, py::return_value_policy::reference)
        .def("update_status", &Person::updateStatus);

    py::class_<Microcell, MicrocellPtr>(m, "Microcell")
        .def("persons", &Microcell::people,
            py::return_value_policy::reference)
        .def("compartment_count", &Microcell::compartmentCount,
            py::return_value_policy::copy);

    py::class_<Cell, CellPtr>(m, "Cell")
        .def("microcells", &Cell::microcells,
            py::return_value_policy::reference)
        .def("persons", &Cell::people,
            py::return_value_policy::reference)
        .def("compartment_count", &Cell::compartmentCount,
            py::return_value_policy::copy)
        .def("location", &Cell::location,
            py::return_value_policy::reference);

    py::class_<Population, PopulationPtr>(m, "Population")
        .def("cells", &Population::cells,
            py::return_value_policy::reference)
        .def("initialize", &Population::initialize);


    py::class_<Household, HouseholdPtr>(m, "Household")
        .def("microcell_pos", &Household::microcellPos, py::return_value_policy::copy);


    py::class_<PopulationFactory>(m, "PopulationFactory")
        .def(py::init<>())
        .def("make_population",
            py::overload_cast<size_t, size_t, size_t>(&PopulationFactory::makePopulation),
            "Basic Factory for Populations",
            py::return_value_policy::take_ownership);

    py::class_<ToyPopulationFactory>(m, "ToyPopulationFactory")
        .def(py::init<>())
        .def("make_population", &ToyPopulationFactory::makePopulation,
            "Factory for creating Toy Populations",
            py::return_value_policy::take_ownership);

    py::class_<HouseholdLinker>(m, "HouseholdLinker")
        .def(py::init<>())
        .def("link_households", &HouseholdLinker::linkHouseholds);
}


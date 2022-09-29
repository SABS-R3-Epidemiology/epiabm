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
        .def_readwrite("age_group", &PersonParams::age_group)
        .def_readwrite("susceptibility", &PersonParams::susceptibility)
        .def_readwrite("infectiousness", &PersonParams::infectiousness)
        .def_readwrite("initial_infectiousness", &PersonParams::initial_infectiousness)
        .def_readwrite("next_status", &PersonParams::next_status)
        .def_readwrite("next_status_time", &PersonParams::next_status_time);
    py::class_<Person, PersonPtr>(m, "Person")
        .def("status", &Person::status, py::return_value_policy::copy)
        .def("params", &Person::params, py::return_value_policy::reference)
        .def("cell_pos", &Person::cellPos, py::return_value_policy::copy)
        .def("microcell_pos", &Person::microcellPos, py::return_value_policy::copy)
        .def("microcell", &Person::microcell, py::return_value_policy::copy)
        .def("places", &Person::places, py::return_value_policy::reference)
        .def("add_place", [](Person& p, PopulationPtr population, CellPtr cell, size_t place_index, size_t group)
            { p.addPlace(*population, cell.get(), place_index, group); })
        .def("remove_place", [](Person& p, PopulationPtr population, CellPtr cell, size_t place_index, size_t group)
            { p.removePlace(*population, cell.get(), place_index, group); })
        .def("remove_place_all_groups", [](Person& p, PopulationPtr population, CellPtr cell, size_t place_index)
            { p.removePlaceAllGroups(*population, cell.get(), place_index); })
        .def("household", &Person::household, py::return_value_policy::copy)
        .def("set_household", &Person::setHousehold, py::return_value_policy::reference)
        .def("set_status", &Person::setStatus)
        .def("update_status", &Person::updateStatus);

    py::class_<Microcell, MicrocellPtr>(m, "Microcell")
        .def("persons", &Microcell::people,
            py::return_value_policy::reference)
        .def("compartment_count", &Microcell::compartmentCount,
            py::return_value_policy::copy)
        .def("households", &Microcell::households,
            py::return_value_policy::reference)
        .def("get_person", [](Microcell& mcell, CellPtr cell, size_t i)
            { return mcell.getPerson(*cell, i); },
            py::return_value_policy::reference)
        .def("get_household", &Microcell::getHousehold,
            py::return_value_policy::reference)
        .def("index", &Microcell::cellPos);

    py::class_<Cell, CellPtr>(m, "Cell")
        .def("microcells", &Cell::microcells,
            py::return_value_policy::reference)
        .def("persons", &Cell::people,
            py::return_value_policy::reference)
        .def("compartment_count", &Cell::compartmentCount,
            py::return_value_policy::copy)
        .def("get_person", &Cell::getPerson,
            py::return_value_policy::reference)
        .def("get_microcell", &Cell::getMicrocell,
            py::return_value_policy::reference)
        .def("set_location", &Cell::setLocation)
        .def("location", &Cell::location,
            py::return_value_policy::reference)
        .def("mark_infectious", &Cell::markInfectious)
        .def("mark_non_infectious", &Cell::markNonInfectious)
        .def("mark_exposed", &Cell::markExposed)
        .def("mark_recovered", &Cell::markRecovered)
        .def("mark_dead", &Cell::markDead)
        .def("index", &Cell::index);

    py::class_<Population, PopulationPtr>(m, "Population")
        .def("cells", &Population::cells,
            py::return_value_policy::reference)
        .def("places", &Population::places,
            py::return_value_policy::reference)
        .def("get_place", [](PopulationPtr population, size_t i)
            { return population->places()[i]; })
        .def("get_cell", [](PopulationPtr population, size_t i)
            { return population->cells()[i]; })
        .def("initialize", &Population::initialize);

    py::class_<HouseholdParams>(m, "HouseholdParams")
        .def_readwrite("susceptibility", &HouseholdParams::susceptibility)
        .def_readwrite("infectiousness", &HouseholdParams::infectiousness)
        .def_readwrite("location", &HouseholdParams::location);
    py::class_<Household, HouseholdPtr>(m, "Household")
        .def("params", &Household::params, py::return_value_policy::reference)
        .def("microcell_pos", &Household::microcellPos, py::return_value_policy::copy)
        .def("is_member", &Household::isMember, py::return_value_policy::copy)
        .def("add_member", &Household::addMember, py::return_value_policy::copy)
        .def("members", &Household::members, py::return_value_policy::reference);

    py::class_<Place, PlacePtr>(m, "Place")
        .def("index", &Place::populationPos, py::return_value_policy::copy)
        .def("is_member", &Place::isMember, py::return_value_policy::copy)
        .def("add_member", &Place::addMember, py::return_value_policy::copy)
        .def("remove_member", &Place::removeMember, py::return_value_policy::copy)
        .def("remove_member_all_groups", &Place::removeMemberAllGroups, py::return_value_policy::copy)
        .def("members", &Place::members, py::return_value_policy::reference)
        .def("members_in_group", &Place::membersInGroup, py::return_value_policy::reference)
        .def("member_groups", &Place::memberGroups, py::return_value_policy::reference);


    py::class_<PopulationFactory>(m, "PopulationFactory")
        .def(py::init<>())
        .def("make_population",
            py::overload_cast<size_t, size_t, size_t>(&PopulationFactory::makePopulation),
            "Basic Factory for Populations",
            py::return_value_policy::take_ownership)
        .def("make_empty_population",
            py::overload_cast<>(&PopulationFactory::makePopulation),
            "Create an Empty Population",
            py::return_value_policy::take_ownership)
        .def("add_cell", &PopulationFactory::addCell)
        .def("add_cells", &PopulationFactory::addCells)
        .def("add_microcell",
            [](PopulationFactory& f, CellPtr cell)
            { f.addMicrocell(cell.get()); })
        .def("add_microcells",
            [](PopulationFactory& f, CellPtr cell, size_t n)
            { f.addMicrocells(cell.get(), n); })
        .def("add_person",
            [](PopulationFactory& f, CellPtr cell, Microcell& mCell)
            { f.addPerson(cell.get(), mCell.cellPos()); })
        .def("add_persons",
            [](PopulationFactory& f, CellPtr cell, Microcell& mCell, size_t n)
            { f.addPeople(cell.get(), mCell.cellPos(), n); })
        .def("add_household",
            [](PopulationFactory& f, Microcell& mCell)
            { f.addHousehold(&mCell); })
        .def("add_households",
            [](PopulationFactory f, Microcell& mCell, size_t n)
            { f.addHouseholds(&mCell, n); })
        .def("add_place", &PopulationFactory::addPlace)
        .def("add_places", &PopulationFactory::addPlaces);

    py::class_<ToyPopulationFactory>(m, "ToyPopulationFactory")
        .def(py::init<>())
        .def("make_population", 
            &ToyPopulationFactory::makePopulation,
            "Factory for creating Toy Populations",
            py::arg("population_size"), py::arg("n_cells"), py::arg("n_mcells_per_cell"), py::arg("n_households"), py::arg("n_places"), py::arg("seed") = 0,
            py::return_value_policy::take_ownership);

    py::class_<HouseholdLinker>(m, "HouseholdLinker")
        .def(py::init<>())
        .def("link_households", &HouseholdLinker::linkHouseholds,
            "Randomly Link Households",
            py::arg("population"), py::arg("n_households"), py::arg("perc_in_households"), py::arg("seed") = 0);
}


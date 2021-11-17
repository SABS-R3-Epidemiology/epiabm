#include "dataclasses/population.hpp"
#include "dataclasses/cell.hpp"
#include "dataclasses/microcell.hpp"
#include "dataclasses/person.hpp"
#include "dataclasses/place.hpp"

#include "factory.hpp"

#include "python_converter.hpp"

#include <boost/python.hpp>
#include <boost/python/enum.hpp>
#include <boost/python/numpy.hpp>
#include <functional>


BOOST_PYTHON_MODULE(covidsim)
{
    using namespace boost::python;

    Py_Initialize();

    class_<seir::Factory>("Factory", init<>())
        .def("print", &seir::Factory::print, "")
        .def("make_population", &seir::Factory::makePopulation, "")
        .def("add_cell", &seir::Factory::addCell, "")
        .def("add_cells", &seir::Factory::addCells, "")
        .def("add_microcell", &seir::Factory::addMicrocell, "")
        .def("add_microcells", &seir::Factory::addMicrocells, "")
        .def("add_person", &seir::Factory::addPerson, "")
        .def("add_people", &seir::Factory::addPeople, "");
    
    class_<seir::Population, seir::PopulationPtr>("Population", no_init)
        .def("print", &seir::Population::print, "")
        .def("for_each_cell", &seir::Population::forEachCell, "")
        .def("get_cell", &seir::Population::getCell,
            return_value_policy<reference_existing_object>(), "");

    class_<seir::Cell, seir::CellPtr>("Cell", no_init)
        .def("print", &seir::Cell::print, "")
        .def("for_each_microcell", &seir::Cell::forEachMicrocell, "")
        .def("for_each_person", &seir::Cell::forEachPerson, "")
        .def("get_microcell", &seir::Cell::getMicrocell,
            return_value_policy<reference_existing_object>(), "")
        .def("get_person", &seir::Cell::getPerson,
            return_value_policy<reference_existing_object>(), "")
        .def("process_new_exposures", &seir::Cell::processNewExposures, "");

    class_<seir::Microcell, seir::MicrocellPtr>("Microcell", no_init)
        .def("print", &seir::Microcell::print, "")
        .def("for_each_person", &seir::Microcell::forEachPerson, "")
        .def("get_person", &seir::Microcell::getPerson,
            return_value_policy<reference_existing_object>(), "");

    class_<seir::Person, seir::PersonPtr>("Person", no_init)
        .def("print", &seir::Person::print, "")
        .def("status", &seir::Person::status, "")
        .def("params", &seir::Person::params,
            return_internal_reference<>())
        .def("set_status", &seir::Person::setStatus, "")
        .def("mark_exposed", &seir::Person::markExposed, "");

    class_<seir::Place, seir::PlacePtr>("Place", no_init);

    class_<seir::PersonParams>("PersonPrams")
        .def_readwrite("age", &seir::PersonParams::age)
        .def_readwrite("susceptible", &seir::PersonParams::susceptibility)
        .def_readwrite("infectiousness", &seir::PersonParams::infectiousness);

    enum_<seir::InfectionStatus>("InfectionStatus")
        .value("Susceptible", seir::InfectionStatus::Susceptible)
        .value("Exposed", seir::InfectionStatus::Exposed)
        .value("InfectASympt", seir::InfectionStatus::InfectASympt)
        .value("InfectMild", seir::InfectionStatus::InfectMild)
        .value("InfectGP", seir::InfectionStatus::InfectGP)
        .value("InfectHosp", seir::InfectionStatus::InfectHosp)
        .value("InfectICU", seir::InfectionStatus::InfectICU)
        .value("InfectICURecov", seir::InfectionStatus::InfectICURecov)
        .value("Recovered", seir::InfectionStatus::Recovered)
        .value("Dead", seir::InfectionStatus::Dead);

    function_converter()
        .from_python<void(int)>()
        .from_python<void(std::string)>()
        .from_python<bool(seir::CellPtr)>()
        .from_python<bool(seir::MicrocellPtr)>()
        .from_python<bool(seir::PersonPtr)>()
        .from_python<bool(seir::PlacePtr)>()
        ;

}
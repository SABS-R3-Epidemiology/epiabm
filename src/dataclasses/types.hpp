#ifndef _COVIDSIM_DATASTRUCTURES_TYPES_HPP
#define _COVIDSIM_DATASTRUCTURES_TYPES_HPP

#include <memory>

namespace seir
{
    class Population;
    typedef std::shared_ptr<Population> PopulationPtr;

    class Cell;
    typedef std::shared_ptr<Cell> CellPtr;

    class Microcell;
    typedef std::shared_ptr<Microcell> MicrocellPtr;

    class Person;
    typedef std::shared_ptr<Person> PersonPtr;

    class Place;
    typedef std::shared_ptr<Place> PlacePtr;

    class Factory;

    enum class InfectionStatus
    {
        Susceptible,
        Exposed,
        InfectASympt,
        InfectMild,
        InfectGP,
        InfectHosp,
        InfectICU,
        InfectICURecov,
        Recovered,
        Dead
    };

} // namespace seir


#endif // _COVIDSIM_DATASTRUCTURES_TYPES_HPP
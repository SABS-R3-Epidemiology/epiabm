#ifndef _COVIDSIM_DATACLASSES_MICROCELL_HPP
#define _COVIDSIM_DATACLASSES_MICROCELL_HPP

#include "types.hpp"

#include <boost/function.hpp>

#include <vector>
#include <memory>
#include <functional>
#include <exception>
#include <iostream>

namespace seir
{

    class Microcell
    {
    private:
        std::vector<PersonPtr> m_people;
        std::vector<PlacePtr> m_places;

        CellPtr m_cell;
        
    public:
        Microcell(CellPtr cell);

        CellPtr cell() { return m_cell; }

        void forEachPerson(boost::function<bool(PersonPtr)> callback);
        void forEachPlace(boost::function<bool(PlacePtr)> callback);

        Person* getPerson(int i) { return m_people[i].get(); }

        void print() { std::cout << "Microcell with " << m_people.size() << " people." << std::endl;}

    private:
        friend class Factory;
        friend class Person;
        friend class Cell;
    };

} // namespace seir

#endif // _COVIDSIM_DATACLASSES_MICROCELL_HPP
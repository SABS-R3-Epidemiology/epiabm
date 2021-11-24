#ifndef _EPIABM_DATACLASSES_MICROCELL_HPP
#define _EPIABM_DATACLASSES_MICROCELL_HPP

#include "types.hpp"

#include <vector>
#include <memory>
#include <functional>
#include <exception>
#include <iostream>

namespace epiabm
{

    class Microcell
    {
    private:
        std::vector<PersonPtr> m_people;
        std::vector<PlacePtr> m_places;

        std::weak_ptr<Cell> m_cell;

        size_t m_listPos;
        
    public:
        Microcell(std::weak_ptr<Cell> cell, size_t listPos);
        ~Microcell() = default;

        CellPtr cell() { return m_cell.lock(); }

        void forEachPerson(std::function<bool(PersonPtr)>& callback);
        void forEachPersonPair(std::function<bool(PersonPtr, PersonPtr)>& callback);
        void forEachPlace(std::function<bool(PlacePtr)>& callback);

        PersonPtr getPerson(int i) { return m_people[i]; }

        void print() { std::cout << "Microcell with " << m_people.size() << " people." << std::endl;}

        std::vector<PersonPtr>& people() { return m_people; }
        std::vector<PlacePtr>& places() { return m_places; }
        
    private:
        friend class Factory;
        friend class Person;
        friend class Cell;
    };

} // namespace epiabm

#endif // _EPIABM_DATACLASSES_MICROCELL_HPP
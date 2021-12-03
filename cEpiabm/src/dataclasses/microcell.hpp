#ifndef _EPIABM_DATACLASSES_MICROCELL_HPP
#define _EPIABM_DATACLASSES_MICROCELL_HPP

#include "person.hpp"
#include "place.hpp"

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
        std::vector<Person*> m_people;
        std::vector<Place> m_places;

        size_t m_cellPos;
        
    public:
        Microcell(size_t cellPos);
        ~Microcell() = default;

        size_t cellPos() { return m_cellPos; }

        void forEachPerson(std::function<bool(Person*)>& callback);
        void forEachPlace(std::function<bool(Place*)>& callback);

        Person& getPerson(size_t i) { return *m_people[i]; }

        void print() { std::cout << "Microcell with " << m_people.size() << " people." << std::endl;}

        std::vector<Person*>& people() { return m_people; }
        std::vector<Place>& places() { return m_places; }
        
    private:
        friend class Factory;
        friend class Person;
        friend class Cell;
    };

    typedef std::shared_ptr<Microcell> MicrocellPtr;

} // namespace epiabm

#endif // _EPIABM_DATACLASSES_MICROCELL_HPP
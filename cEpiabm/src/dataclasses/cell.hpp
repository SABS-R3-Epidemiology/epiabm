#ifndef _EPIABM_DATACLASSES_CELL_HPP
#define _EPIABM_DATACLASSES_CELL_HPP

#include "microcell.hpp"
#include "person.hpp"

#include <vector>
#include <memory>
#include <functional>
#include <iostream>
#include <queue>

namespace epiabm
{
    
    class Cell
    {
    private:
        std::vector<Person> m_people;
        std::vector<Microcell> m_microcells;
        size_t m_numInfected;

        //std::queue<int> m_personQueue;

        std::vector<size_t> m_peopleSorted; // Vector of people indices with 1st n_infectious as infectious, rest as non-infectious
        std::vector<size_t> m_peopleSortedInv; // Vector to map between person's index in m_people and m_peopleStatesSorted

    public:
        Cell();
        ~Cell() = default;

        void forEachMicrocell(std::function<bool(Microcell*)>& callback);
        void forEachPerson(std::function<bool(Person*)>& callback);
        void forEachInfectious(std::function<bool(Person*)>& callback);
        void forEachNonInfectious(std::function<bool(Person*)>& callback);

        Person& getPerson(size_t i) { return m_people[i]; }
        Microcell& getMicrocell(size_t i) { return m_microcells[i]; }

        void print() { std::cout << "Cell with " << m_microcells.size() << " microcells and " << m_people.size() << " people." << std::endl; }
        
        //void processQueue(std::function<void(Person*)> callback);
        //void enqueuePerson(Person* person) { m_personQueue.push(person->cellPos()); }

        std::vector<Person>& people() { return m_people; }
        std::vector<Microcell>& microcells() { return m_microcells; }

        void markInfectious(Person* person);
        void markNonInfectious(Person* person);

    private:
        friend class PopulationFactory;
    };
    
    typedef std::shared_ptr<Cell> CellPtr;

} // namespace epiabm

#endif // _EPIABM_DATACLASSES_CELL_HPP
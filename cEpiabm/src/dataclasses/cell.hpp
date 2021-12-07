#ifndef EPIABM_DATACLASSES_CELL_HPP
#define EPIABM_DATACLASSES_CELL_HPP

#include "microcell.hpp"
#include "person.hpp"

#include <vector>
#include <memory>
#include <functional>
#include <queue>


namespace epiabm
{
    
    class Cell
    {
    private:
        std::vector<Person> m_people;
        std::vector<Microcell> m_microcells;
        size_t m_numInfectious;

        std::queue<size_t> m_personQueue;
        std::set<size_t> m_peopleInQueue;

        std::vector<size_t> m_peopleSorted; // Vector of people indices with 1st n_infectious as infectious, rest as non-infectious
        std::vector<size_t> m_peopleSortedInv; // Vector to map between person's index in m_people and m_peopleStatesSorted

    public:
        Cell();
        ~Cell() = default;
        Cell(const Cell&) = default;
        Cell(Cell&&) = default;

        void forEachMicrocell(std::function<bool(Microcell*)> callback);
        void forEachPerson(std::function<bool(Person*)> callback);
        void forEachInfectious(std::function<bool(Person*)> callback);
        void forEachNonInfectious(std::function<bool(Person*)> callback);

        Person& getPerson(size_t i);
        Microcell& getMicrocell(size_t i);

        void processQueue(std::function<void(size_t)> callback);
        bool enqueuePerson(size_t personIndex);

        std::vector<Person>& people();
        std::vector<Microcell>& microcells();

        void initializeInfectiousGrouping();
        bool markInfectious(size_t personIndex);
        bool markNonInfectious(size_t personIndex);
        size_t numInfectious() const;

    private:
        friend class Microcell;
        friend class Place;
    };
    
    typedef std::shared_ptr<Cell> CellPtr;

} // namespace epiabm

#endif // EPIABM_DATACLASSES_CELL_HPP
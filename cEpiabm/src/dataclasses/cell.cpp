
#include "cell.hpp"

#include <iostream>


namespace epiabm
{

    Cell::Cell() :
        m_people(),
        m_microcells(),
        m_numInfectious(0),
        m_personQueue(),
        m_peopleInQueue(),
        m_peopleSorted(),
        m_peopleSortedInv()
    {}

    void Cell::forEachMicrocell(std::function<bool(Microcell*)> callback)
    {
        for (size_t i = 0; i < m_microcells.size(); i++)
        {
            if (!callback(&m_microcells[i])) return;
        }
    }

    void Cell::forEachPerson(std::function<bool(Person*)> callback)
    {
        for (size_t i = 0; i < m_people.size(); i++)
        {
            if (!callback(&m_people[i])) return;
        }
    }

    void Cell::forEachInfectious(std::function<bool(Person*)> callback)
    {
        for (size_t i = 0; i < m_numInfectious; i++)
        {
            if (!callback(&m_people[m_peopleSorted[i]])) return;
        }
    }

    void Cell::forEachNonInfectious(std::function<bool(Person*)> callback)
    {
        for (size_t i = m_numInfectious; i < m_people.size(); i++)
        {
            if (!callback(&m_people[m_peopleSorted[i]])) return;
        }
    }

    Person& Cell::getPerson(size_t i) { return m_people[i]; }
    Microcell& Cell::getMicrocell(size_t i) { return m_microcells[i]; }

    void Cell::processQueue(std::function<void(size_t)> callback)
    {
        while (!m_personQueue.empty())
        {
            callback(m_personQueue.front());
            m_personQueue.pop();
        }
        m_peopleInQueue.clear();
    }

    bool Cell::enqueuePerson(size_t personIndex)
    {
        if (m_peopleInQueue.find(personIndex) != m_peopleInQueue.end()) return false;
        m_personQueue.push(personIndex);
        m_peopleInQueue.insert(personIndex);
        return true;
    }

    std::vector<Person>& Cell::people() { return m_people; }
    std::vector<Microcell>& Cell::microcells() { return m_microcells; }

    void Cell::initializeInfectiousGrouping()
    {
        m_peopleSorted = std::vector<size_t>(m_people.size());
        m_peopleSortedInv = std::vector<size_t>(m_people.size());
        for (size_t i = 0; i < m_people.size(); i++)
        {
            m_peopleSortedInv[i] = i;
            m_peopleSorted[i] = i;
        }
    }

    bool Cell::markInfectious(size_t newInfected)
    {
        if (m_peopleSortedInv[newInfected] < m_numInfectious) return false; // Person already in infected section
        size_t swapTarget = m_peopleSorted[m_numInfectious]; // Index of swap target in m_people

        std::swap(m_peopleSorted[m_peopleSortedInv[newInfected]],
            m_peopleSorted[m_numInfectious]); // Swap new infected and target in sorted vector
        m_peopleSortedInv[swapTarget] = m_peopleSortedInv[newInfected]; // New location of target in sorted = old position of newly infected
        m_peopleSortedInv[newInfected] = m_numInfectious; // New location of newly infected is m_numInfected;

        m_numInfectious++; // Increment number of infected
        return true;
    }

    bool Cell::markNonInfectious(size_t oldInfected)
    {
        if (m_peopleSortedInv[oldInfected] >= m_numInfectious) return false; // Person already in non-infected
        size_t swapTarget = m_peopleSorted[m_numInfectious - 1]; // Index of swap target (last infectious person)

        std::swap(m_peopleSorted[m_peopleSortedInv[oldInfected]],
            m_peopleSorted[m_numInfectious - 1]);
        m_peopleSortedInv[swapTarget] = m_peopleSortedInv[oldInfected]; // New location of swap target is old position of previously infected
        m_peopleSortedInv[oldInfected] = m_numInfectious - 1;

        m_numInfectious--;
        return true;
    }

    size_t Cell::numInfectious() const { return m_numInfectious; }

} // namespace epiabm

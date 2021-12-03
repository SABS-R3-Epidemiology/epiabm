
#include "cell.hpp"

namespace epiabm
{

    Cell::Cell() :
        m_people(),
        m_microcells(),
        m_numInfected(0),
        //m_personQueue(),
        m_peopleSorted(),
        m_peopleSortedInv()
    {}

    void Cell::forEachMicrocell(std::function<bool(Microcell*)>& callback)
    {
        for (size_t i = 0; i < m_microcells.size(); i++)
        {
            callback(&m_microcells[i]);
        }
    }

    void Cell::forEachPerson(std::function<bool(Person*)>& callback)
    {
        for (size_t i = 0; i < m_people.size(); i++)
        {
            callback(&m_people[i]);
        }
    }

    void Cell::forEachInfectious(std::function<bool(Person*)>& callback)
    {
        for (size_t i = 0; i < m_numInfected; i++)
        {
            callback(&m_people[m_peopleSorted[i]]);
        }
    }

    void Cell::forEachNonInfectious(std::function<bool(Person*)>& callback)
    {
        for (size_t i = m_numInfected; i < m_people.size(); i++)
        {
            callback(&m_people[m_peopleSorted[i]]);
        }
    }
/*
    void Cell::processQueue(std::function<void(Person*)> callback)
    {
        while (!m_personQueue.empty())
        {
            callback(&m_people[m_personQueue.front()]);
            m_personQueue.pop();
        }
    }*/

    void Cell::markInfectious(Person* person)
    {
        size_t newInfected = person->cellPos(); // New infected person's index in m_people
        size_t swapTarget = m_peopleSorted[m_numInfected]; // Index of swap target in m_people
        
        std::swap(m_peopleSorted[m_peopleSortedInv[newInfected]],
            m_peopleSorted[m_numInfected]); // Swap new infected and target in sorted vector
        m_peopleSortedInv[swapTarget] = m_peopleSortedInv[newInfected]; // New location of target in sorted = old position of newly infected
        m_peopleSortedInv[newInfected] = m_numInfected; // New location of newly infected is m_numInfected;

        m_numInfected++; // Increment number of infected
    }

    void Cell::markNonInfectious(Person* person)
    {
        size_t oldInfected = person->cellPos(); // Index of person no longer infectious
        size_t swapTarget = m_peopleSorted[m_numInfected - 1]; // Index of swap target (last infectious person)

        std::swap(m_peopleSorted[m_peopleSortedInv[oldInfected]],
            m_peopleSorted[m_numInfected - 1]);
        m_peopleSortedInv[swapTarget] = m_peopleSortedInv[oldInfected]; // New location of swap target is old position of previously infected
        m_peopleSortedInv[oldInfected] = m_numInfected - 1;

        m_numInfected--;
    }

} // namespace epiabm

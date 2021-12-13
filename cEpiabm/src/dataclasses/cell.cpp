
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

    /**
     * @brief Apply Callback to each person in Queue
     * Also Clears the queue
     * @param callback 
     */
    void Cell::processQueue(std::function<void(size_t)> callback)
    {
        while (!m_personQueue.empty()) // loop through queue
        {
            callback(m_personQueue.front());
            m_personQueue.pop();
        }
        m_peopleInQueue.clear(); // Remove person from the set of people currently in queue
    }

    /**
     * @brief Add person to queue
     * Same person cannot be queued twice.
     * @param personIndex 
     * @return true Person successfully queued.
     * @return false Person reject because already in queue.
     */
    bool Cell::enqueuePerson(size_t personIndex)
    {
        if (m_peopleInQueue.find(personIndex) != m_peopleInQueue.end()) return false; // if person already queued
        m_personQueue.push(personIndex); // add to queue
        m_peopleInQueue.insert(personIndex); // insert into queued set
        return true;
    }

    std::vector<Person>& Cell::people() { return m_people; }
    std::vector<Microcell>& Cell::microcells() { return m_microcells; }

    /**
     * @brief Initialize framework for fast looping through infectious / susceptible
     * Cell can maintain a vector of people where all the infectious are at the start.
     * This is to allow quick looping through only infectious people without looping through all people and checking their status.
     */
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

    /**
     * @brief Mark Person as Infectious for Fast Looping through Infectious People
     * Mark a person as infectious. Used for fast looping through infectious or non-infectious people without looping through all people and checking their statuses.
     * Cell::initializeInfectiousGroupings must have been called once before for this function to be used.
     * @param newInfected Person who is becoming infectious.
     * @return true Successfully changed person's state to infectious.
     * @return false Person was already infectious.
     */
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

    /**
     * @brief Mark Person as Non-Infectious for Fast Looping through Infectious People
     * Mark a person as non-infectious. Used for fast looping through infectious or non-infectious people without looping through all people and checking their statuses.
     * Cell::initializeInfectiousGroupings must have been called once before this can be used.
     * @param oldInfected Person who is no longer infectious.
     * @return true Successfully changed person's state to non-infectious.
     * @return false Person was already marked as non-infectious.
     */
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

    /**
     * @brief Get Number of Infectious
     * Get number of currently infectious people.
     * This corresponds to the number of infectious being maintained by the cell for fast looping through infectious / non-infectious.
     * Cell::initializeInfectiousGroupings() must have been called once before this can be used.
     * @return size_t Number of infectious
     */
    size_t Cell::numInfectious() const { return m_numInfectious; }

} // namespace epiabm

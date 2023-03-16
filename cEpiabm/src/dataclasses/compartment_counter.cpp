
#include "compartment_counter.hpp"
#include "person.hpp"
#include "cell.hpp"

#include <vector>
#include <iostream>

namespace epiabm
{
    /**
     * @brief Construct a new Compartment Counter object
     * 
     */
    CompartmentCounter::CompartmentCounter() :
        m_counts()
    {}

    /**
     * @brief Destroy the Compartment Counter:: Compartment Counter object
     * 
     */
    CompartmentCounter::~CompartmentCounter()
    {}

    /**
     * @brief Reset the compartment counts
     * 
     */
    void CompartmentCounter::clear()
    {
        m_counts.clear();
    }

    /**
     * @brief Retrieve the number of people in a specific compartment
     * 
     * @param status Which compartment to retrieve the count for
     * @return unsigned int Number of people in the compartment
     */
    unsigned int CompartmentCounter::operator()(InfectionStatus status) const
    {
        if (m_counts.find(status) != m_counts.end()) return m_counts.at(status);
        else return 0;
    }

    /**
     * @brief Notify the compartment counter that someone's status has changed
     * 
     * @param oldStatus Person's previous status
     * @param newStatus Person's new status
     */
    void CompartmentCounter::notify(InfectionStatus old_status, InfectionStatus new_status)
    {
        m_counts[old_status]--;
        m_counts[new_status]++;
    }

    /**
     * @brief Initialize the compartment counter on a cell
     * Used for initializing a microcell's compartment counter
     * Takes a cell and list of people indices for initialization on microcells
     * Since microcells store a subset of cell person indices
     * @param cell Parent cell
     * @param people Person indices being tracked (people within microcell)
     */
    void CompartmentCounter::initialize(Cell* cell, const std::vector<size_t>& people)
    {
        clear();
        for (const auto pi : people)
            m_counts[cell->getPerson(pi).status()]++;
    }

    /**
     * @brief Initialize the compartment counter
     * Used for initializing a cell's compartment counter
     * @param people List of people to keep track of
     */
    void CompartmentCounter::initialize(const std::vector<Person>& people)
    {
        clear();
        for (const auto& p : people)
            m_counts[p.status()]++;
    }

}

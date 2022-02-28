#ifndef EPIABM_DATACLASSES_COMPARTMENT_COUNTER_HPP
#define EPIABM_DATACLASSES_COMPARTMENT_COUNTER_HPP

#include "infection_status.hpp"
#include "person.hpp"

#include <map>
#include <vector>

namespace epiabm
{
    class Cell;

    /**
     * @brief Class to keep count of number of people in each compartment
     * 
     */
    class CompartmentCounter
    {
    private:
        std::map<InfectionStatus, unsigned int> m_counts;
        
    public:
        /**
         * @brief Construct a new Compartment Counter object
         * 
         */
        CompartmentCounter();
        ~CompartmentCounter() = default;

        /**
         * @brief Reset the compartment counts
         * 
         */
        void clear();
        /**
         * @brief Retrieve the number of people in a specific compartment
         * 
         * @param status Which compartment to retrieve the count for
         * @return unsigned int Number of people in the compartment
         */
        unsigned int operator()(InfectionStatus status) const;

        /**
         * @brief Notify the compartment counter that someone's status has changed
         * 
         * @param oldStatus Person's previous status
         * @param newStatus Person's new status
         */
        void notify(InfectionStatus oldStatus, InfectionStatus newStatus);

        /**
         * @brief Initialize the compartment counter on a cell
         * Used for initializing a microcell's compartment counter
         * Takes a cell and list of people indices for initialization on microcells
         * Since microcells store a subset of cell person indices
         * @param cell Parent cell
         * @param people Person indices being tracked (people within microcell)
         */
        void initialize(Cell* cell, const std::vector<size_t>& people);
        /**
         * @brief Initialize the compartment counter
         * Used for initializing a cell's compartment counter
         * @param people List of people to keep track of
         */
        void initialize(const std::vector<Person>& people);

    private:
    };


} // namespace epiabm

#endif // EPIABM_DATACLASSES_COMPARTMENT_COUNTER_HPP

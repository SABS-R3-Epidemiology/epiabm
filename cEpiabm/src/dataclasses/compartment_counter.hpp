#ifndef EPIABM_DATACLASSES_COMPARTMENT_COUNTER_HPP
#define EPIABM_DATACLASSES_COMPARTMENT_COUNTER_HPP

#include "infection_status.hpp"
#include "person.hpp"

#include <map>
#include <unordered_map>
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

        std::unordered_map<InfectionStatus, unsigned int> m_counts;
        
    public:
        CompartmentCounter();
        ~CompartmentCounter();

        void clear();

        unsigned int operator()(InfectionStatus status) const;

        void notify(InfectionStatus oldStatus, InfectionStatus newStatus);

        void initialize(Cell* cell, const std::vector<size_t>& people);
        
        void initialize(const std::vector<Person>& people);

    private:

        friend class Cell;
        friend class Microcell;
    };


} // namespace epiabm

#endif // EPIABM_DATACLASSES_COMPARTMENT_COUNTER_HPP

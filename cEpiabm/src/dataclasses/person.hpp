#ifndef EPIABM_DATACLASSES_PERSON_HPP
#define EPIABM_DATACLASSES_PERSON_HPP

#include "infection_status.hpp"

#include <vector>
#include <memory>
#include <optional>
#include <set>
#include <functional>

namespace epiabm
{
    class Place;
    class Cell;
    class Population;

    struct PersonParams
    {
        unsigned char age_group = 0;
        float susceptibility = 0, infectiousness = 0;
        
        unsigned short next_status_time = 0;
        InfectionStatus next_status = InfectionStatus::Susceptible;
        float initial_infectiousness = 0;
        unsigned short infection_start_timestep = 0;
    };

    class Person
    {
    private:
        InfectionStatus m_status;

        PersonParams m_params;

        size_t m_cellPos; // Position of person within Cell::m_people;
        size_t m_mcellPos; // Position of person within Microcell::m_people;
        size_t m_household = 0; // Household's index within Microcell::m_household;
        size_t m_microcell; // Microcell's index within Cell::m_microcells;
        bool m_hasHousehold; // flag for whether the household has been set;

        std::set<std::pair<size_t, size_t>> m_places; // Indices of Places which the person is a member of;
        // Each place is represented by a pair (place_index, group)

    public:
        Person(size_t microcell, size_t cellPos, size_t mcellPos);
        ~Person();
        //Person(const Person&) = default;
        //Person(Person&&) = default;

        InfectionStatus status() const;
        PersonParams& params();

        // Force set status (For configuring population) - Population has to be re-initialized if this is called
        void setStatus(const InfectionStatus status);
        // Update status method (For changing a person's status during simulation)
        void updateStatus(Cell* cell, const InfectionStatus status, const unsigned short timestep);

        size_t cellPos() const;
        size_t microcellPos() const;
        size_t microcell() const;
        
        bool setHousehold(size_t hh);
        std::optional<size_t> household();

        void addPlace(Population& population, Cell* cell, size_t place_index, size_t group);
        void removePlace(Population& population, Cell* cell ,size_t place_index, size_t group=0);
        void removePlaceAllGroups(Population& population, Cell* cell, size_t place_index);

        std::set<std::pair<size_t, size_t>>& places();
        /**
         * @brief Loop through each place
         * Callback provides the place and group within place that the person is part of
         * 
         * @param population 
         * @param callback 
         */
        void forEachPlace(Population& population, std::function<void(Place*, size_t)> callback);

    private:
    };
    
    typedef std::shared_ptr<Person> PersonPtr;

} // namespace epiabm

#endif // EPIABM_DATACLASSES_PERSON_HPP

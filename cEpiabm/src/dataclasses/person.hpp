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
        float initial_infectiousness;
        unsigned short infection_start_timestep;
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

        std::set<size_t> m_places; // Indices of Places which the person is a member of;

    public:
        Person(size_t microcell, size_t cellPos, size_t mcellPos);
        ~Person();
        //Person(const Person&) = default;
        //Person(Person&&) = default;

        InfectionStatus status() const;
        PersonParams& params();

        void updateStatus(Cell* cell, const InfectionStatus status, const unsigned short timestep);

        size_t cellPos() const;
        size_t microcellPos() const;
        size_t microcell() const;
        
        bool setHousehold(size_t hh);
        std::optional<size_t> household();

        std::set<size_t>& places();
        void forEachPlace(Population& population, std::function<void(Place*)> callback);

    private:
    };
    
    typedef std::shared_ptr<Person> PersonPtr;

} // namespace epiabm

#endif // EPIABM_DATACLASSES_PERSON_HPP

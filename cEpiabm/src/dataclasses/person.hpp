#ifndef EPIABM_DATACLASSES_PERSON_HPP
#define EPIABM_DATACLASSES_PERSON_HPP

#include <vector>
#include <memory>
#include <optional>

namespace epiabm
{

    struct PersonParams
    {
        unsigned char age = 0;
        float susceptibility = 0, infectiousness = 0;
    };

    enum class InfectionStatus
    {
        Susceptible,
        Exposed,
        InfectASympt,
        InfectMild,
        InfectGP,
        InfectHosp,
        InfectICU,
        InfectICURecov,
        Recovered,
        Dead
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
        bool m_hasHousehold = false; // flag for whether the household has been set;

    public:
        Person(size_t microcell, size_t cellPos, size_t mcellPos);
        ~Person() = default;
        Person(const Person&) = default;
        Person(Person&&) = default;

        InfectionStatus status() const;
        PersonParams& params();

        void updateStatus(InfectionStatus status);

        size_t cellPos() const;
        size_t microcellPos() const;
        size_t microcell() const;
        
        bool setHousehold(size_t hh);
        std::optional<size_t> household();

    private:
    };
    
    typedef std::shared_ptr<Person> PersonPtr;

} // namespace epiabm

#endif // EPIABM_DATACLASSES_PERSON_HPP

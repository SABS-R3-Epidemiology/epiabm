#ifndef EPIABM_DATACLASSES_PERSON_HPP
#define EPIABM_DATACLASSES_PERSON_HPP

#include <vector>
#include <memory>
#include <iostream>

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

        size_t m_cellPos;
        size_t m_mcellPos;
        size_t m_household = 0;
        bool m_hasHousehold = false;

    public:
        Person(size_t cellPos, size_t mcellPos);
        ~Person() = default;
        Person(const Person&) = default;
        Person(Person&&) = default;

        InfectionStatus status() const { return m_status; }
        PersonParams& params() { return m_params; }

        void print() { std::cout << "Person, cellPos: " << m_cellPos
            << ", mcellPos: " << m_mcellPos  
            << std::endl; }

        void setStatus(InfectionStatus status) { m_status = status; }

        size_t cellPos() const { return m_cellPos; }
        size_t microcellPos() const { return m_mcellPos; }
        
        bool setHousehold(size_t hh);
        size_t household() { return m_household; }

    private:
    };
    
    typedef std::shared_ptr<Person> PersonPtr;

} // namespace epiabm

#endif // EPIABM_DATACLASSES_PERSON_HPP

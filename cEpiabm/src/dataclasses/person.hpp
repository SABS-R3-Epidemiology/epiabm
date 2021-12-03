#ifndef _EPIABM_DATACLASSES_PERSON_HPP
#define _EPIABM_DATACLASSES_PERSON_HPP

#include "infection_status.hpp"

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

    class Person
    {
    public:
        InfectionStatus m_status;

        PersonParams m_params;

        size_t m_cellPos;
        size_t m_mcellPos;

    public:
        Person(size_t cellPos, size_t mcellPos);
        ~Person() = default;
        Person(const Person&) = default;
        Person(Person&&) = default;

        InfectionStatus status() const { return m_status; }
        PersonParams& params() { return m_params; }

        void print() { std::cout << "A Person!" << std::endl; }

        void setStatus(InfectionStatus status) { m_status = status; }

        size_t microcellPos() { return m_mcellPos; }
        size_t cellPos() { return m_cellPos; }

    private:
        friend class Factory;
        friend class Microcell;
        friend class Cell;
    };
    
    typedef std::shared_ptr<Person> PersonPtr;

} // namespace epiabm

#endif // _EPIABM_DATACLASSES_PERSON_HPP

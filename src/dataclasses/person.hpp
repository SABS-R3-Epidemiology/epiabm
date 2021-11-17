#ifndef _COVIDSIM_DATACLASSES_PERSON_HPP
#define _COVIDSIM_DATACLASSES_PERSON_HPP

#include "types.hpp"
#include "cell.hpp"
#include "microcell.hpp"

#include <vector>
#include <memory>
#include <iostream>

namespace seir
{

    struct PersonParams
    {
        unsigned char age = 0;
        float susceptibility = 0, infectiousness = 0;
    };

    class Person
    {
    private:
        MicrocellPtr m_microcell;
        InfectionStatus m_status;

        PersonParams m_params;

    public:
        Person(MicrocellPtr microcell);
        ~Person() = default;
        Person(const Person&) = default;
        Person(Person&&) = default;

        MicrocellPtr microcell() const { return m_microcell; }

        InfectionStatus status() const { return m_status; }
        PersonParams& params() { return m_params; }
        unsigned char age() const { return m_params.age; }
        float susceptibility() const { return m_params.susceptibility; }
        float infectiousness() const { return m_params.infectiousness; }

        void print() { std::cout << "A Person!" << std::endl; }

        void markExposed() { m_microcell->m_cell->addNewExposure(this); };

        void setStatus(InfectionStatus status) { m_status = status; }

    private:
        friend class Factory;
        friend class Microcell;
        friend class Cell;
    };
} // namespace seir

#endif // _COVIDSIM_DATACLASSES_PERSON_HPP

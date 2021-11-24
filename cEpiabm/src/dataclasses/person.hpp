#ifndef _EPIABM_DATACLASSES_PERSON_HPP
#define _EPIABM_DATACLASSES_PERSON_HPP

#include "types.hpp"
#include "cell.hpp"
#include "microcell.hpp"

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
        std::weak_ptr<Microcell> m_microcell;
        InfectionStatus m_status;

        PersonParams m_params;

        size_t m_listPos;

    public:
        Person(std::weak_ptr<Microcell> microcell, size_t listPos);
        ~Person() = default;
        Person(const Person&) = default;
        Person(Person&&) = default;

        unsigned char age;
        float susceptibility, infectiousness;

        InfectionStatus status() const { return m_status; }
        PersonParams& params() { return m_params; }

        void print() { std::cout << "A Person!" << std::endl; }

        void setStatus(InfectionStatus status) { m_status = status; }

        MicrocellPtr microcell() { return m_microcell.lock(); }
        CellPtr cell() { return m_microcell.lock()->cell(); }

    private:
        friend class Factory;
        friend class Microcell;
        friend class Cell;
    };
} // namespace epiabm

#endif // _EPIABM_DATACLASSES_PERSON_HPP

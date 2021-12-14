#include "person.hpp"

#include <iostream>

namespace epiabm
{

    Person::Person(size_t cellPos, size_t mcellPos) :
        m_status(InfectionStatus::Susceptible),
        m_params(PersonParams()),
        m_cellPos(cellPos),
        m_mcellPos(mcellPos)
    {}

    InfectionStatus Person::status() const { return m_status; }
    PersonParams& Person::params() { return m_params; }

    void Person::setStatus(InfectionStatus status) { m_status = status; }

    size_t Person::cellPos() const { return m_cellPos; }
    size_t Person::microcellPos() const { return m_mcellPos; }

    bool Person::setHousehold(size_t hh)
    {
        if (m_hasHousehold)
            return false;
        m_household = hh;
        m_hasHousehold = true;
        return true;
    }

    size_t Person::household() { return m_household; }

} // namespace epiabm

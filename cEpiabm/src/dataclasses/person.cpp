#include "person.hpp"

#include <iostream>

namespace epiabm
{

    Person::Person(size_t microcell, size_t cellPos, size_t mcellPos) :
        m_status(InfectionStatus::Susceptible),
        m_params(PersonParams()),
        m_cellPos(cellPos),
        m_mcellPos(mcellPos),
        m_microcell(microcell)
    {}

    InfectionStatus Person::status() const { return m_status; }
    PersonParams& Person::params() { return m_params; }

    void Person::updateStatus(InfectionStatus status) { m_status = status; }

    size_t Person::cellPos() const { return m_cellPos; }
    size_t Person::microcellPos() const { return m_mcellPos; }
    size_t Person::microcell() const { return m_microcell; }

    bool Person::setHousehold(size_t hh)
    {
        if (m_hasHousehold)
            return false;
        m_household = hh;
        m_hasHousehold = true;
        return true;
    }

    std::optional<size_t> Person::household()
    { return m_hasHousehold? m_household : std::optional<size_t>(); }

} // namespace epiabm

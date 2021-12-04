#include "person.hpp"

namespace epiabm
{

    Person::Person(size_t cellPos, size_t mcellPos) :
            m_status(InfectionStatus::Susceptible),
            m_params(PersonParams()),
            m_cellPos(cellPos),
            m_mcellPos(mcellPos)
    {}

    bool Person::setHousehold(size_t hh)
    {
        if (m_hasHousehold) return false;
        m_household = hh; m_hasHousehold = true;
        return true;
    }

} // namespace epiabm


#include "household.hpp"


namespace epiabm
{

    Household::Household(size_t mcellPos) :
        MembersInterface(mcellPos),
        m_params(),
        m_mcellPos(mcellPos)
    {}

    size_t Household::microcellPos() const { return m_mcellPos; }

    HouseholdParams& Household::params() { return m_params; }

} // namespace epiabm

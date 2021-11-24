#include "person.hpp"

namespace epiabm
{

    Person::Person(std::weak_ptr<Microcell> microcell, size_t listPos) :
            m_listPos(listPos),
            m_microcell(microcell),
            m_params(PersonParams()),
            m_status(InfectionStatus::Susceptible)
    {}

} // namespace epiabm

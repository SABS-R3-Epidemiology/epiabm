#include "person.hpp"

namespace seir
{

    Person::Person(MicrocellPtr microcell) :
            m_microcell(microcell),
            m_params(PersonParams()),
            m_status(InfectionStatus::Susceptible)
    {}

} // namespace seir

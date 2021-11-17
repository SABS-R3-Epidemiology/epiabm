
#include "cell.hpp"
#include "person.hpp"

namespace seir
{

    Cell::Cell() :
        m_people(0),
        m_microcells(0)
    {}

    void Cell::forEachMicrocell(boost::function<bool(MicrocellPtr)> callback)
    {
        for (size_t i = 0; i < m_microcells.size(); i++)
        {
            callback(m_microcells[i]);
        }
    }

    void Cell::forEachPerson(boost::function<bool(PersonPtr)> callback)
    {
        for (size_t i = 0; i < m_people.size(); i++)
        {
            callback(m_people[i]);
        }
    }

    void Cell::processNewExposures()
    {
        while (!m_newExposures.empty())
        {
            Person* person = m_newExposures.front();
            person->m_status = InfectionStatus::Exposed;
            m_newExposures.pop();
        }
    }

} // namespace seir

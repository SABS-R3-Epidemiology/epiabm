
#include "cell.hpp"
#include "person.hpp"

namespace epiabm
{

    Cell::Cell() :
        m_people(0),
        m_microcells(0)
    {}

    void Cell::forEachMicrocell(std::function<bool(MicrocellPtr)>& callback)
    {
        for (size_t i = 0; i < m_microcells.size(); i++)
        {
            callback(m_microcells[i]);
        }
    }

    void Cell::forEachPerson(std::function<bool(PersonPtr)>& callback)
    {
        for (size_t i = 0; i < m_people.size(); i++)
        {
            callback(m_people[i]);
        }
    }

    void Cell::forEachInfectious(std::function<bool(PersonPtr)>& callback)
    {
        for (size_t i = 0; i < m_numInfected; i++)
        {
            callback(m_people[i]);
        }
    }

    void Cell::forEachNonInfectious(std::function<bool(PersonPtr)>& callback)
    {
        for (size_t i = m_numInfected; i < m_people.size(); i++)
        {
            callback(m_people[i]);
        }
    }

    void Cell::processQueue(std::function<void(PersonPtr)> callback)
    {
        while (!m_personQueue.empty())
        {
            callback(m_personQueue.front().lock());
            m_personQueue.pop();
        }
    }

    void Cell::markInfectious(PersonPtr person)
    {
        std::swap(m_people[person->m_listPos], m_people[m_numInfected]);
        m_people[person->m_listPos]->m_listPos = person->m_listPos;
        m_people[m_numInfected]->m_listPos = m_numInfected++;
    }

    void Cell::markNonInfectious(PersonPtr person)
    {
        std::swap(m_people[person->m_listPos], m_people[m_numInfected]);
        m_people[person->m_listPos]->m_listPos = person->m_listPos;
        m_people[m_numInfected]->m_listPos = m_numInfected--;
    }

} // namespace epiabm

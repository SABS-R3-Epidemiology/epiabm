
#include "microcell.hpp"

namespace epiabm
{

    Microcell::Microcell(std::weak_ptr<Cell> cell, size_t listPos) :
        m_listPos(listPos),
        m_cell(cell),
        m_people(0),
        m_places(0)
    {}

    void Microcell::forEachPerson(std::function<bool(PersonPtr)>& callback)
    {
        for (size_t i = 0; i < m_people.size(); i++)
        {
            callback(m_people[i]);
        }
    }

    void Microcell::forEachPersonPair(std::function<bool(PersonPtr, PersonPtr)>& callback)
    {
        for (size_t i = 0; i < m_people.size(); i++)
        {
            for (size_t j = i; j < m_people.size(); j++)
            {
                callback(m_people[i], m_people[j]);
            }
        }
    }

    void Microcell::forEachPlace(std::function<bool(PlacePtr)>& callback)
    {
        for (size_t i = 0; i < m_places.size(); i++)
        {
            callback(m_places[i]);
        }
    }

} // namespace epiabm

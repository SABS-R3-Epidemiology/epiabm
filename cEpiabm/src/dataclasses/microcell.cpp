
#include "microcell.hpp"

namespace epiabm
{

    Microcell::Microcell(size_t cellPos) :
        m_people(),
        m_places(),
        m_cellPos(cellPos)
    {}

    void Microcell::forEachPerson(std::function<bool(Person*)>& callback)
    {
        for (size_t i = 0; i < m_people.size(); i++)
        {
            callback(m_people[i]);
        }
    }

    void Microcell::forEachPlace(std::function<bool(Place*)>& callback)
    {
        for (size_t i = 0; i < m_places.size(); i++)
        {
            callback(&m_places[i]);
        }
    }

} // namespace epiabm

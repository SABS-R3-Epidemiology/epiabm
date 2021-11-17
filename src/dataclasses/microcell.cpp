
#include "microcell.hpp"

namespace seir
{

    Microcell::Microcell(CellPtr cell) :
        m_cell(cell),
        m_people(0),
        m_places(0)
    {}

    void Microcell::forEachPerson(boost::function<bool(PersonPtr)> callback)
    {
        for (size_t i = 0; i < m_people.size(); i++)
        {
            callback(m_people[i]);
        }
    }

    void Microcell::forEachPlace(boost::function<bool(PlacePtr)> callback)
    {
        for (size_t i = 0; i < m_places.size(); i++)
        {
            callback(m_places[i]);
        }
    }

} // namespace seir

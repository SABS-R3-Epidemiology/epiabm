
#include "place.hpp"
#include "cell.hpp"
#include "microcell.hpp"

namespace epiabm
{

    Place::Place(size_t mcellPos) :
        m_members(),
        m_mcellPos(mcellPos)
    {}

    void Place::forEachMember(Cell& cell, Microcell& microcell, std::function<bool(Person*)>& callback)
    {
        auto it = m_members.begin();
        while (it != m_members.end())
        {
            if (!callback(&cell.people()[microcell.people()[*it]])) return;
        }
    }

} // namespace epiabm

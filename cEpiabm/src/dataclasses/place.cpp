
#include "place.hpp"
#include "cell.hpp"
#include "population.hpp"

namespace epiabm
{

    Place::Place(size_t mPos) :
        m_mPos(mPos)
    {}

    size_t Place::populationPos() const { return m_mPos; }

    void Place::forEachMember(Population& population,
        std::function<bool(Person*)> callback)
    {
        for (const auto& p : m_members)
            if (!callback(&population.cells()[p.first]->getPerson(p.second))) return;
    }

    bool Place::isMember(size_t cell, size_t person) const
    {
        return m_members.find(std::make_pair(cell, person)) != m_members.end();
    }

    bool Place::addMember(size_t cell, size_t person)
    {
        std::pair<size_t, size_t> r = std::make_pair(cell, person);
        if (m_members.find(r) != m_members.end())
            return false;
        m_members.insert(r);
        return true;
    }

    std::set<std::pair<size_t, size_t>>& Place::members()
    {
        return m_members;
    }

} // namespace epiabm

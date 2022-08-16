
#include "place.hpp"
#include "cell.hpp"
#include "population.hpp"

namespace epiabm
{

    Place::Place(size_t mPos) :
        m_mPos(mPos),
        m_members(),
        m_memberGroups()
    {}

    size_t Place::populationPos() const { return m_mPos; }

    void Place::forEachMember(Population& population,
        std::function<bool(Cell*,Person*)> callback)
    {
        for (const auto& p : m_members)
            if (!callback(
                population.cells()[p.first.first].get(),
                &population.cells()[p.first.first]->getPerson(p.first.second)))
                return;
    }

    void Place::forEachMemberInGroup(Population& population, size_t group,
        std::function<bool(Cell*,Person*)> callback)
    {
        for (const auto& p : m_memberGroups[group])
            if (!callback(
                population.cells()[p.first].get(),
                &population.cells()[p.first]->getPerson(p.second)))
                return;
    }

    void Place::forEachMemberGroup(Population&,
        std::function<bool(size_t, const std::set<std::pair<size_t,size_t>>&)> callback)
    {
        for (const auto& g : m_memberGroups)
            if (!callback(g.first, g.second)) return;
    }

    bool Place::sampleMembersInGroup(Population& population, size_t group, size_t n,
        std::function<void(Cell*, Person*)> callback, std::mt19937_64& rg)
    {
        if (m_memberGroups[group].size() < 1){
            return false;
        }
        std::vector<std::pair<size_t, size_t>> chosen;
        std::sample(m_memberGroups[group].begin(), m_memberGroups[group].end(),
            std::back_inserter(chosen), n, rg);
        for (const auto& r : chosen)
            callback(population.cells()[r.first].get(),
                    &population.cells()[r.first]->getPerson(r.second));
        return true;
    }

    bool Place::isMember(size_t cell, size_t person) const
    {
        auto p = std::make_pair(cell, person);
        return m_members.find(p) == m_members.end() ? false :
            m_members.at(p) > 0;
    }

    bool Place::addMember(size_t cell, size_t person, size_t group)
    {
        std::pair<size_t, size_t> r = std::make_pair(cell, person);
        if (m_memberGroups[group].find(r) == m_memberGroups[group].end())
        {
            m_members[r] += 1;
            m_memberGroups[group].insert(r);
            return true;
        }
        return false;
    }

    bool Place::removeMemberAllGroups(size_t cell, size_t person)
    {
        std::vector<size_t> groups;
        for (const auto& g : m_memberGroups) groups.push_back(g.first);
        for (const auto& g : groups)
        {
            removeMember(cell, person, g);
            if (!isMember(cell, person)) break;
        }
        return true;
    }

    bool Place::removeMember(size_t cell, size_t person, size_t group)
    {
        std::pair<size_t, size_t> p = std::make_pair(cell, person);
        if (m_memberGroups[group].find(p) != m_memberGroups[group].end())
        {
            m_memberGroups[group].erase(p);
            m_members[p]-=1;
            if (m_members[p] <= 0) m_members.erase(p);
            return true;
        }
        return false;
    }

    std::map<std::pair<size_t, size_t>, size_t>& Place::members()
    {
        return m_members;
    }

    std::set<std::pair<size_t, size_t>>& Place::membersInGroup(size_t group)
    {
        return m_memberGroups[group];
    }

    std::map<size_t, std::set<std::pair<size_t, size_t>>>& Place::memberGroups()
    {
        return m_memberGroups;
    }

} // namespace epiabm

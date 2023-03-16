
#include "place.hpp"
#include "cell.hpp"
#include "population.hpp"

namespace epiabm
{

    /**
     * @brief Construct a new Place:: Place object
     * 
     * @param mPos Position of place within population's places vector.
     */
    Place::Place(size_t mPos) :
        m_mPos(mPos),
        m_members(),
        m_memberGroups()
    {}

    /**
     * @brief Get index of place within population's places vector
     * 
     * @return size_t Index of place within population's places vector
     */
    size_t Place::populationPos() const { return m_mPos; }

    /**
     * @brief Loop through all members in the place
     * 
     * Irrespective of place group
     * Callback can return false to terminate loop early
     * 
     * @param population Reference to parent population
     * @param callback Callback to apply to each member of the place
     */
    void Place::forEachMember(Population& population,
        std::function<bool(Cell*,Person*)> callback)
    {
        for (const auto& p : m_members)
            if (!callback(
                population.cells()[p.first.first].get(),
                &population.cells()[p.first.first]->getPerson(p.first.second)))
                return;
    }

    /**
     * @brief Loop through each member in specific place group
     * 
     * Callback can return false to terminate loop early
     * 
     * @param population Reference to parent population
     * @param group Group number to retrieve members from
     * @param callback Callback to apply to each member in place's group
     */
    void Place::forEachMemberInGroup(Population& population, size_t group,
        std::function<bool(Cell*,Person*)> callback)
    {
        for (const auto& p : m_memberGroups[group])
            if (!callback(
                population.cells()[p.first].get(),
                &population.cells()[p.first]->getPerson(p.second)))
                return;
    }

    /**
     * @brief Loop through each member group
     * Callback provides group number and set of people in the group
     * People in group defined by pairs (cell index, person's index in cell)
     * 
     * @param population Reference to parent population
     * @param callback Callback to apply to member group
     */
    void Place::forEachMemberGroup(Population&,
        std::function<bool(size_t, const std::set<std::pair<size_t,size_t>>&)> callback)
    {
        for (const auto& g : m_memberGroups)
            if (!callback(g.first, g.second)) return;
    }

    /**
     * @brief Randomly sample n members in place with specific group number
     * 
     * If n is larger than number of people in specific place group, all members in that group are returned
     * 
     * @param population Reference to parent group
     * @param group Place's group number to retrieve members from
     * @param n Number of members to sample
     * @param callback Callback to apply to each sampled member
     * @param rg Random number generator to use
     * @return true Success
     * @return false Returns false if there are no people in specified place group.
     */
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

    /**
     * @brief Check if person is a member of the place
     * 
     * @param cell Index of cell within population's cells vector
     * @param person Index of person within cell's people vector
     * @return true Person is a member of the place
     * @return false Person is not a member of the place
     */
    bool Place::isMember(size_t cell, size_t person) const
    {
        auto p = std::make_pair(cell, person);
        return m_members.find(p) == m_members.end() ? false :
            m_members.at(p) > 0;
    }

    /**
     * @brief Add person to a place group
     * 
     * @param cell Index of person's cell within population's cells vector
     * @param person Index of person within cell's people vector
     * @param group Place group number to add person to
     * @return true Successfully added person to place group
     * @return false Person is already a part of that place group
     */
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

    /**
     * @brief Remove person from the place
     * 
     * Irrespective of group number
     * 
     * @param cell Index of person's cell within population's cells vector
     * @param person Index of person within parent cell's people vector
     * @return true
     * @return false 
     */
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

    /**
     * @brief Remove person from a specific place group
     * 
     * @param cell Index of person's cell within population's cells vector
     * @param person Index of person within parent cell's people vector
     * @param group Place group number to remove person from
     * @return true Successfully removed
     * @return false Person wasn't part of the place group
     */
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

    /**
     * @brief Get reference to place's members
     * 
     * Map of person (cell index, person index) to number of groups that person is part of.
     * 
     * @return std::map<std::pair<size_t, size_t>, size_t>& Reference to place's members map
     */
    std::map<std::pair<size_t, size_t>, size_t>& Place::members()
    {
        return m_members;
    }

    /**
     * @brief Get reference to set of members in a place group
     * 
     * @param group Place group number
     * @return std::set<std::pair<size_t, size_t>>& Set of (cell index, person index) members in place group.
     */
    std::set<std::pair<size_t, size_t>>& Place::membersInGroup(size_t group)
    {
        return m_memberGroups[group];
    }

    /**
     * @brief Get reference to all place groups
     * 
     * Map of place group number to set of (cell index, person index) members part of that place group
     * 
     * @return std::map<size_t, std::set<std::pair<size_t, size_t>>>& 
     */
    std::map<size_t, std::set<std::pair<size_t, size_t>>>& Place::memberGroups()
    {
        return m_memberGroups;
    }

} // namespace epiabm

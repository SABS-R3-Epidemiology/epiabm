#ifndef EPIABM_DATACLASSES_PLACE_HPP
#define EPIABM_DATACLASSES_PLACE_HPP

#include "person.hpp"

#include <memory>
#include <set>
#include <map>
#include <functional>
#include <random>

namespace epiabm
{
    const size_t N_PLACE_GROUPS = 4;

    class Cell;
    class Population;

    /**
     * @brief Class to represent a place
     * 
     */
    class Place
    {
    private:
        size_t m_mPos; // Position of Place in Population's vector of places

        std::map<std::pair<size_t, size_t>, size_t> m_members; // Set of pairs representing members. Each pair is (cell index, person index)
        // Changed to a map to keep count of number groups member is a part of

        std::map<size_t, std::set<std::pair<size_t, size_t>>> m_memberGroups; // Groups people within a place (allows the Place class to represent a place type, and groups within the place the different locations of a place type)

    public:
        Place(size_t mPos);
        ~Place() = default;

        size_t populationPos() const;

        void forEachMember(Population& population,
            std::function<bool(Cell*,Person*)> callback);
        void forEachMemberInGroup(Population& population, size_t group,
            std::function<bool(Cell*,Person*)> callback);
        void forEachMemberGroup(Population& population,
            std::function<bool(size_t, const std::set<std::pair<size_t, size_t>>&)> callback);

        bool sampleMembersInGroup(
            Population& population,
            size_t group,
            size_t n,
            std::function<void(Cell*, Person*)> callback,
            std::mt19937_64& rg);

        bool isMember(size_t cell, size_t person) const;

        bool addMember(size_t cell, size_t person, size_t group=0); // Maybe should make this private

        bool removeMemberAllGroups(size_t cell, size_t person); // Remove person from all groups
        bool removeMember(size_t cell, size_t person, size_t group=0);

        std::map<std::pair<size_t, size_t>, size_t>& members();

        std::set<std::pair<size_t, size_t>>& membersInGroup(size_t group=0);

        std::map<size_t, std::set<std::pair<size_t, size_t>>>& memberGroups();

    private:
        friend class PopulationFactory;
    };

    typedef std::shared_ptr<Place> PlacePtr;

} // namespace epiabm

#endif // EPIABM_DATACLASSES_PLACE_HPP

#ifndef EPIABM_DATACLASSES_PLACE_HPP
#define EPIABM_DATACLASSES_PLACE_HPP

#include "person.hpp"

#include <memory>
#include <set>
#include <functional>

namespace epiabm
{

    class Cell;
    class Population;

    class Place
    {
    private:
        size_t m_mPos; // Position of Place in Population's vector of places

        std::set<std::pair<size_t, size_t>> m_members; // Set of pairs representing members. Each pair is (cell index, person index)

    public:
        Place(size_t mPos);
        ~Place() = default;

        size_t populationPos() const;

        void forEachMember(Population& population,
            std::function<bool(Person*)> callback);
        bool isMember(size_t cell, size_t person) const;

        bool addMember(size_t cell, size_t person); // Maybe should make this private

        std::set<std::pair<size_t, size_t>>& members();

    private:
        friend class PopulationFactory;
    };

    typedef std::shared_ptr<Place> PlacePtr;

} // namespace epiabm

#endif // EPIABM_DATACLASSES_PLACE_HPP

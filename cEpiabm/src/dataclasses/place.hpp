#ifndef EPIABM_DATACLASSES_PLACE_HPP
#define EPIABM_DATACLASSES_PLACE_HPP

#include "infection_status.hpp"
#include "person.hpp"

#include <vector>
#include <set>
#include <functional>

namespace epiabm
{
    class Cell;
    class Microcell;

    class Place
    {
    private:
        std::set<size_t> m_members;
        size_t m_mcellPos;

        std::pair<double, double> m_location;

    public:
        Place(size_t mcellPos);

        size_t microcellPos() { return m_mcellPos; }
        std::pair<double, double> location() { return m_location; }

        void forEachMember(Cell& cell, Microcell& microcell, std::function<bool(Person*)>& callback);
        bool isMember(size_t person) { return m_members.find(person) != m_members.end(); }

        void addMember(size_t person) { m_members.insert(person); }

    private:
        friend class Factory;
    };

    typedef std::shared_ptr<Place> PlacePtr;

} // namespace epiabm

#endif // EPIABM_DATACLASSES_PLACE_HPP

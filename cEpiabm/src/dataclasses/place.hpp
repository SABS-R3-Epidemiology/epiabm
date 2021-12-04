#ifndef EPIABM_DATACLASSES_PLACE_HPP
#define EPIABM_DATACLASSES_PLACE_HPP

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
        std::set<size_t> m_members; // Location of people in Microcell::m_people vector
        size_t m_mcellPos;

    public:
        Place(size_t mcellPos);

        size_t microcellPos() const { return m_mcellPos; }

        void forEachMember(Cell& cell, Microcell& microcell, std::function<bool(Person*)>& callback);
        bool isMember(size_t person) { return m_members.find(person) != m_members.end(); }

        bool addMember(size_t person); // Maybe should make this private

        std::set<size_t>& members() { return m_members; }

    private:
        friend class Factory;
    };

    typedef std::shared_ptr<Place> PlacePtr;

} // namespace epiabm

#endif // EPIABM_DATACLASSES_PLACE_HPP

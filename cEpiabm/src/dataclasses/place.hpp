#ifndef _EPIABM_DATACLASSES_PLACE_HPP
#define _EPIABM_DATACLASSES_PLACE_HPP

#include "infection_status.hpp"
#include "person.hpp"

#include <vector>
#include <set>
#include <functional>

namespace epiabm
{

    class Place
    {
    private:
        std::set<Person*> m_members;
        size_t m_mcellPos;

        std::pair<double, double> m_location;

    public:
        Place(size_t mcellPos);

        size_t microcellPos() { return m_mcellPos; }
        std::pair<double, double> location() { return m_location; }

        void forEachMember(std::function<bool(Person*)>& callback);
        bool isMember(Person* person);

        void addMember(Person* person) { m_members.insert(person); }

    private:
        friend class Factory;
    };

    typedef std::shared_ptr<Place> PlacePtr;

} // namespace epiabm

#endif // _EPIABM_DATACLASSES_PLACE_HPP
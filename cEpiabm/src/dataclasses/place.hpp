#ifndef _EPIABM_DATACLASSES_PLACE_HPP
#define _EPIABM_DATACLASSES_PLACE_HPP

#include "types.hpp"

#include <vector>
#include <set>
#include <functional>

namespace epiabm
{

    class Place
    {
    private:
        std::set<PersonPtr> m_members;
        std::weak_ptr<Microcell> m_microcell;

        std::pair<double, double> m_location;

    public:
        Place(MicrocellPtr microcell);

        MicrocellPtr microcell() { return m_microcell.lock(); }
        std::pair<double, double> location() { return m_location; }

        void forEachMember(std::function<bool(PersonPtr)>& callback);
        bool isMember(PersonPtr person);

        void addMember(PersonPtr person) { m_members.insert(person); }

    private:
        friend class Factory;
    };

} // namespace epiabm

#endif // _EPIABM_DATACLASSES_PLACE_HPP
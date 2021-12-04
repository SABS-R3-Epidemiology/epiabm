#ifndef EPIABM_DATACLASSES_MEMBERS_INTERFACE_HPP
#define EPIABM_DATACLASSES_MEMBERS_INTERFACE_HPP

#include "person.hpp"

#include <set>
#include <functional>
#include <memory>

namespace epiabm
{
    class Cell;
    class Microcell;

    class MembersInterface
    {
    protected:
        std::set<size_t> m_members; // Indices of people in Microcell::m_people vector

    public:
        MembersInterface(size_t mcellPos);
        virtual ~MembersInterface() {}

        virtual void forEachMember(Cell &cell, Microcell &microcell, std::function<bool(Person *)> callback);
        virtual bool isMember(size_t person) const { return m_members.find(person) != m_members.end(); }

        virtual bool addMember(size_t person); // Maybe should make this private

        virtual std::set<size_t> &members() { return m_members; }

    private:
        size_t m_mcellPos;
    };

    typedef std::shared_ptr<MembersInterface> MembersInterfacePtr;

} // epiabm

#endif // EPIABM_DATACLASSES_MEMBERS_INTERFACE_HPP
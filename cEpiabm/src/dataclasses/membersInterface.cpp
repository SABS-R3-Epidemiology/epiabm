
#include "membersInterface.hpp"
#include "cell.hpp"
#include "microcell.hpp"

namespace epiabm
{

    MembersInterface::MembersInterface() :
        m_members()
    {}

    void MembersInterface::forEachMember(Cell& cell, Microcell& microcell, std::function<bool(Person*)> callback)
    {
        auto it = m_members.begin();
        while (it != m_members.end())
        {
            if (!callback(&cell.people()[microcell.people()[*it]]))
                return;
            it++;
        }
    }

    bool MembersInterface::isMember(size_t person) const
    {
        return m_members.find(person) != m_members.end();
    }

    bool MembersInterface::addMember(size_t person)
    {
        if (m_members.find(person) != m_members.end())
            return false;
        m_members.insert(person);
        return true;
    }

    std::set<size_t>& MembersInterface::members()
    {
        return m_members;
    }

} // namespace epiabm
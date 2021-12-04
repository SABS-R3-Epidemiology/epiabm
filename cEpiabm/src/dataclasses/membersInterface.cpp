
#include "membersInterface.hpp"
#include "cell.hpp"
#include "microcell.hpp"

namespace epiabm
{

MembersInterface::MembersInterface(size_t mcellPos) :
    m_members(),
    m_mcellPos(mcellPos)
{}

void MembersInterface::forEachMember(Cell &cell, Microcell &microcell, std::function<bool(Person *)> callback)
{
    auto it = m_members.begin();
    while (it != m_members.end())
    {
        if (!callback(&cell.people()[microcell.people()[*it]]))
            return;
        it++;
    }
}

bool MembersInterface::addMember(size_t person)
{
    if (m_members.find(person) != m_members.end())
        return false;
    m_members.insert(person);
    return true;
}

} // namespace epiabm

#include "household.hpp"
#include "cell.hpp"
#include "microcell.hpp"


namespace epiabm
{

    Household::Household(size_t mcellPos) :
        m_members(),
        m_params(),
        m_mcellPos(mcellPos)
    {}

    void Household::forEachMember(Cell& cell, Microcell& microcell, std::function<bool(Person*)> callback)
    {
        auto it = m_members.begin();
        while (it != m_members.end())
        {
            if (!callback(&cell.people()[microcell.people()[*it]])) return;
            it++;
        }
    }

    bool Household::addMember(size_t person)
    {
        if (m_members.find(person) != m_members.end()) return false;
        m_members.insert(person);
        return true;
    }

} // namespace epiabm

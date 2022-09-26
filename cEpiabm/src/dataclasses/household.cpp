
#include "household.hpp"
#include "cell.hpp"
#include "microcell.hpp"

namespace epiabm
{
    /**
     * @brief Construct a new Household object
     * 
     * @param mcellPos Index of the household within the host cell
     */
    Household::Household(size_t mcellPos) :
        m_params(),
        m_mcellPos(mcellPos),
        m_members()
    {}

    /**
     * @brief Getter for the household's index within the host Cell::m_households
     * 
     * @return size_t Household's index within Cell::m_households
     */
    size_t Household::microcellPos() const { return m_mcellPos; }

    /**
     * @brief Getter for household's parameters
     * Used to both access and modify individual household's parameters
     * @return HouseholdParams& 
     */
    HouseholdParams& Household::params() { return m_params; }

    /**
     * @brief Apply callback to each member of the household
     * 
     * Callback can return false to terminate loop early
     * 
     * @param cell Reference to household's cell
     * @param microcell Reference to household's microcell
     * @param callback Callback to apply to each person
     */
    void Household::forEachMember(Cell& cell, Microcell& microcell, std::function<bool(Person*)> callback)
    {
        auto it = m_members.begin();
        while (it != m_members.end())
        {
            if (!callback(&cell.people()[microcell.people()[*it]]))
                return;
            it++;
        }
    }

    /**
     * @brief Check if person is a member of the household
     * 
     * @param person Index of person within microcell
     * @return true 
     * @return false 
     */
    bool Household::isMember(size_t person) const
    {
        return m_members.find(person) != m_members.end();
    }

    /**
     * @brief Add person to the houshold
     * 
     * @param person Index of person within microcell
     * @return true Successfully added person
     * @return false Person already in household
     */
    bool Household::addMember(size_t person)
    {
        if (m_members.find(person) != m_members.end())
            return false;
        m_members.insert(person);
        return true;
    }

    /**
     * @brief Get reference to household's members set
     * 
     * @return std::set<size_t>& Set of person indices. Each entry is an index in Microcell's people vector.
     */
    std::set<size_t>& Household::members()
    {
        return m_members;
    }

} // namespace epiabm

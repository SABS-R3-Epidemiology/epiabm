#ifndef EPIABM_DATACLASSES_HOUSEHOLD_HPP
#define EPIABM_DATACLASSES_HOUSEHOLD_HPP

#include "person.hpp"

#include <tuple>
#include <vector>
#include <set>
#include <functional>

namespace epiabm
{

    struct HouseholdParams
    {
        double susceptibliity = 0, infectiveness = 0;
        std::pair<double, double> location = {0, 0};
    };

    class Cell;
    class Microcell;

    class Household
    {
    private:
        std::set<size_t> m_members; // Indices of people in Microcell::m_people vector
        HouseholdParams m_params;

        size_t m_mcellPos;

    public:
        Household(size_t mcellPos);

        size_t microcellPos() const { return m_mcellPos; }

        HouseholdParams& params() { return m_params; }

        void forEachMember(Cell& cell, Microcell& microcell, std::function<bool(Person*)> callback);
        bool isMember(size_t person) const { return m_members.find(person) != m_members.end(); }

        bool addMember(size_t person); // Maybe should make this private

        std::set<size_t>& members() { return m_members; }

    private:
    };

} // namespace epiabm

#endif // EPIABM_DATACLASSES_HOUSEHOLD_HPP

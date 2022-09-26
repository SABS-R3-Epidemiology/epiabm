#ifndef EPIABM_DATACLASSES_HOUSEHOLD_HPP
#define EPIABM_DATACLASSES_HOUSEHOLD_HPP


#include <tuple>
#include <memory>
#include <set>
#include <functional>

namespace epiabm
{
    class Cell;
    class Microcell;
    class Person;
    /**
     * @brief Structure for household parameters
     * For parameters which are independent to individual households
     */
    struct HouseholdParams
    {
        double susceptibility = 0, infectiousness = 0;
        std::pair<double, double> location = {0, 0};
    };

    /**
     * @brief Class representing a household
     * 
     */
    class Household
    {
    private:
        HouseholdParams m_params;

        size_t m_mcellPos; // Position within Microcell::m_households vector

        std::set<size_t> m_members; // Indices of people in Microcell::m_people vector

    public:
        Household(size_t mcellPos);
        ~Household() = default;

        size_t microcellPos() const;

        HouseholdParams& params();

        void forEachMember(Cell &cell, Microcell &microcell,
            std::function<bool(Person *)> callback);
        bool isMember(size_t person) const;

        bool addMember(size_t person); // Maybe should make this private

        std::set<size_t> &members();
    private:

    friend class PopulationFactory;
    };

    typedef std::shared_ptr<Household> HouseholdPtr;

} // namespace epiabm

#endif // EPIABM_DATACLASSES_HOUSEHOLD_HPP

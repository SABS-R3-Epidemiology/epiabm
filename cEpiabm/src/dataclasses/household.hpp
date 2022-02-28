#ifndef EPIABM_DATACLASSES_HOUSEHOLD_HPP
#define EPIABM_DATACLASSES_HOUSEHOLD_HPP

#include "membersInterface.hpp"

#include <tuple>
#include <memory>

namespace epiabm
{
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
    class Household : public MembersInterface
    {
    private:
        HouseholdParams m_params;

        size_t m_mcellPos; // Position within Microcell::m_households vector

    public:
        /**
         * @brief Construct a new Household object
         * 
         * @param mcellPos Index of the household within the host cell
         */
        Household(size_t mcellPos);
        ~Household() = default;

        /**
         * @brief Getter for the household's index within the host Cell::m_households
         * 
         * @return size_t Household's index within Cell::m_households
         */
        size_t microcellPos() const;

        /**
         * @brief Getter for household's parameters
         * Used to both access and modify individual household's parameters
         * @return HouseholdParams& 
         */
        HouseholdParams& params();
    private:

    friend class PopulationFactory;
    };

    typedef std::shared_ptr<Household> HouseholdPtr;

} // namespace epiabm

#endif // EPIABM_DATACLASSES_HOUSEHOLD_HPP

#ifndef EPIABM_DATACLASSES_HOUSEHOLD_HPP
#define EPIABM_DATACLASSES_HOUSEHOLD_HPP

#include "membersInterface.hpp"

#include <tuple>
#include <memory>

namespace epiabm
{

    struct HouseholdParams
    {
        double susceptibility = 0, infectiousness = 0;
        std::pair<double, double> location = {0, 0};
    };

    class Household : public MembersInterface
    {
    private:
        HouseholdParams m_params;

        size_t m_mcellPos; // Position within Microcell::m_households vector

    public:
        Household(size_t mcellPos);
        ~Household() = default;

        size_t microcellPos() const;

        HouseholdParams& params();
    private:

    friend class PopulationFactory;
    };

    typedef std::shared_ptr<Household> HouseholdPtr;

} // namespace epiabm

#endif // EPIABM_DATACLASSES_HOUSEHOLD_HPP

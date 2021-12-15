#ifndef EPIABM_SWEEPS_HOUSEHOLD_SWEEP_HPP
#define EPIABM_SWEEPS_HOUSEHOLD_SWEEP_HPP

#include "sweep_interface.hpp"

#include <memory>


namespace epiabm
{


    class HouseholdSweep : public SweepInterface
    {
    private:
    public:
        HouseholdSweep();
        ~HouseholdSweep() = default;

        void operator()(const unsigned short timestep) override;

    private:
        bool cellCallback(
            const unsigned short timestep,
            Cell* cell);

        bool cellInfectiousCallback(
            const unsigned short timestep,
            Cell* cell,
            Person* infectious);

        bool infectAttempt(
            const unsigned short timestep,
            Cell* cell, HouseholdPtr household,
            Person* infector, Person* infectee);

    }; // class HouseholdSweep

    typedef std::shared_ptr<HouseholdSweep> HouseholdSweepPtr;


} // namespace epiabm


#endif // EPIABM_SWEEPS_HOUSEHOLD_SWEEP_HPP
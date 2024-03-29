#ifndef EPIABM_SWEEPS_HOUSEHOLD_SWEEP_HPP
#define EPIABM_SWEEPS_HOUSEHOLD_SWEEP_HPP

#include "sweep_interface.hpp"

#include <memory>


namespace epiabm
{

    /**
     * @brief Spread Infection within Households
     * Process each infected person and try to infect all susceptibles in their household.
     * People to be newly infected get queued in their cell's people queue.
     */
    class HouseholdSweep : public SweepInterface
    {
    private:
        unsigned long m_counter;

    public:
        HouseholdSweep(SimulationConfigPtr cfg);
        ~HouseholdSweep() = default;

        /**
         * @brief Perform Household Sweep
         * 
         * @param timestep 
         */
        void operator()(const unsigned short timestep) override;

        bool cellCallback(
            const unsigned short timestep,
            Cell* cell) override;

        bool cellInfectiousCallback(
            const unsigned short timestep,
            Cell* cell,
            Person* infectious);

    private:
        bool infectAttempt(
            const unsigned short timestep,
            Cell* cell, HouseholdPtr household,
            Person* infector, Person* infectee);

        double calcHouseInf(
            Person* infector,
            unsigned short int timestep);

        double calcHouseSusc(
            Person* infector,
            Person* infectee,
            unsigned short int timestep);

        double calcPersonSusc(
            Person* infector,
            Person* infectee,
            unsigned short int timestep);

    }; // class HouseholdSweep

    typedef std::shared_ptr<HouseholdSweep> HouseholdSweepPtr;


} // namespace epiabm


#endif // EPIABM_SWEEPS_HOUSEHOLD_SWEEP_HPP
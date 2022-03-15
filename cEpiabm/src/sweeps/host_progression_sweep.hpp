#ifndef EPIABM_SWEEPS_HOST_PROGRESSION_SWEEP_HPP
#define EPIABM_SWEEPS_HOST_PROGRESSION_SWEEP_HPP

#include "sweep_interface.hpp"

#include <memory>
#include <map>


namespace epiabm
{

    class HostProgressionSweep : SweepInterface
    {
    private:
        

    public:
        HostProgressionSweep(SimulationConfigPtr cfg);
        ~HostProgressionSweep() = default;

        /**
         * @brief Perform Host Progression Sweep
         * 
         * @param timestep 
         */
        void operator()(const unsigned short timestep) override;

        bool cellCallback(
            const unsigned short timestep,
            Cell* cell);

        /* For each Exposed Person */
        bool cellExposedCallback(
            const unsigned short timestep,
            Cell* cell,
            Person* person);

        /* For each Infectious Person */
        bool cellInfectiousCallback(
            const unsigned short timestep,
            Cell* cell,
            Person* person);

    private:
        unsigned short time_to_next_status(
            Person* person,
            InfectionStatus status);

        InfectionStatus first_infectious_status(
            Person* person);

        InfectionStatus next_status(
            Person* person);
    }; // class HostProgressionSweep

    typedef std::shared_ptr<HostProgressionSweep> HostProgressionSweepPtr;

} // namespace epiabm

#endif // EPIABM_SWEEPS_HOST_PROGRESSION_SWEEP_HPP
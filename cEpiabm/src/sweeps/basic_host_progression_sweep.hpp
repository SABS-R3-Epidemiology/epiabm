#ifndef EPIABM_SWEEPS_BASIC_HOST_PROGRESSION_SWEEP_HPP
#define EPIABM_SWEEPS_BASIC_HOST_PROGRESSION_SWEEP_HPP

#include "sweep_interface.hpp"

#include <map>
#include <memory>
#include <stack>

namespace epiabm
{

    /**
     * @brief Replication of Covid-sim's host progression sweep without Severity
     * Checks Person's time to next state.
     * If the time is past, choose next state and update person.
     * Also decides duration to remain in next state.
     */
    class BasicHostProgressionSweep : public SweepInterface
    {
    private:
    public:
        BasicHostProgressionSweep(SimulationConfigPtr cfg);
        ~BasicHostProgressionSweep();

        void operator()(const unsigned short timestep) override;

        bool cellCallback(
            const unsigned short timestep,
            Cell* cell) override;

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

    private:
    };

    typedef std::shared_ptr<BasicHostProgressionSweep> BasicHostProgressionSweepPtr;

} // namespace epiabm


#endif // EPIABM_SWEEPS_BASIC_HOST_PROGRESSION_SWEEP_HPP
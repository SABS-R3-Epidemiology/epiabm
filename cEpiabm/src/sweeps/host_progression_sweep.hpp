#ifndef EPIABM_SWEEPS_HOST_PROGRESSION_SWEEP_HPP
#define EPIABM_SWEEPS_HOST_PROGRESSION_SWEEP_HPP

#include "sweep_interface.hpp"
#include "../utilities/inverse_cdf.hpp"

#include <memory>
#include <vector>
#include <array>
#include <random>

namespace epiabm
{

    class HostProgressionSweep : public SweepInterface
    {
    private:
        std::array<std::array<double, N_INFECTION_STATES>, N_INFECTION_STATES> m_transitionMatrix;
        std::array<std::array<InverseCDF*, N_INFECTION_STATES>, N_INFECTION_STATES> m_transitionTimeMatrix;

        std::mt19937 m_generator;

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
        unsigned short timeToNextStatus(
            Person* person,
            InfectionStatus status);

        InfectionStatus firstInfectionStatus(
            Person* person);

        InfectionStatus chooseNextStatus(
            InfectionStatus prev);

        unsigned short chooseNextTransitionTime(
            InfectionStatus current, InfectionStatus next);

        void loadTransitionMatrix();
        void loadTransitionTimeMatrix();
    }; // class HostProgressionSweep

    typedef std::shared_ptr<HostProgressionSweep> HostProgressionSweepPtr;

} // namespace epiabm

#endif // EPIABM_SWEEPS_HOST_PROGRESSION_SWEEP_HPP
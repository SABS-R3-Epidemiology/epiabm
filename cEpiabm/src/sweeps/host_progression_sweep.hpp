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
        std::array<std::array<std::array<double, N_INFECTION_STATES>, N_INFECTION_STATES>, N_AGE_GROUPS> m_transitionMatrix;
        std::array<std::array<InverseCDF*, N_INFECTION_STATES>, N_INFECTION_STATES> m_transitionTimeMatrix;
        std::vector<double> m_infectiousnessProfile;

        std::mt19937 m_generator;
        std::gamma_distribution<double> m_initialInfectiousnessDistrib;

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
        unsigned short timeToNextStatus(
            Person* person,
            InfectionStatus status);

        InfectionStatus firstInfectionStatus(
            Person* person);

        InfectionStatus chooseNextStatus(
            Person* person, InfectionStatus prev);

        unsigned short chooseNextTransitionTime(
            InfectionStatus current, InfectionStatus next);

        double chooseInfectiousness(
            InfectionStatus status);

        void updateInfectiousness(
            const unsigned short timestep, Person* person);

        void loadTransitionMatrix();
        void loadTransitionTimeMatrix();
        void loadInfectiousnessProfile();
    }; // class HostProgressionSweep

    typedef std::shared_ptr<HostProgressionSweep> HostProgressionSweepPtr;

} // namespace epiabm

#endif // EPIABM_SWEEPS_HOST_PROGRESSION_SWEEP_HPP
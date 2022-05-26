#ifndef EPIABM_SWEEPS_NEW_INFECTION_SWEEP_HPP
#define EPIABM_SWEEPS_NEW_INFECTION_SWEEP_HPP

#include "sweep_interface.hpp"
#include "../dataclasses/person.hpp"
#include "../configuration/simulation_config.hpp"

#include <memory>


namespace epiabm
{

    /**
     * @brief Process New Infections
     * Processes the people queued into each cell, and changes their status from Susceptible to Exposed.
     * This sweep should be called after each of the infection spreading sweeps, which queue people to be infected.
     * Dequeus people as they are moved to exposed.
     * Also marks people as exposed in the Cell for fast looping through subsets.
     */
    class NewInfectionSweep : public SweepInterface
    {
        private:
            unsigned long m_counter;

        public:
            NewInfectionSweep(SimulationConfigPtr cfg);
            ~NewInfectionSweep() = default;

            /**
             * @brief Perform New Infection Processing Sweep
             * 
             * @param timestep 
             */
            void operator()(const unsigned short timestep) override;

            bool cellCallback(
                const unsigned short timestep,
                Cell* cell) override;

            void cellPersonQueueCallback(
                unsigned short timestep,
                Cell* cell,
                size_t personIndex);

        private:
            unsigned short latent_time(Person* person);

    }; // class NewInfectionSweep
    
    typedef std::shared_ptr<NewInfectionSweep> NewInfectionSweepPtr;

} // namespace epiabm


#endif // EPIABM_SWEEPS_NEW_INFECTION_SWEEP_HPP
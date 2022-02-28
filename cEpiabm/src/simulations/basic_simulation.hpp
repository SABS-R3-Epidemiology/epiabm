#ifndef EPIABM_SIMULATINS_BASIC_SIMULATION_HPP
#define EPIABM_SIMULATINS_BASIC_SIMULATION_HPP


#include "../sweeps/sweep_interface.hpp"
#include "../reporters/timestep_reporter_interface.hpp"

#include "../dataclasses/population.hpp"

#include <memory>
#include <vector>


namespace epiabm
{
    /**
     * @brief Master Simulation Controlling Class
     * Links population with sweeps, and runs the sweeps to perform simulation
     * Reporters can be attached to extract information about the simulation
     */
    class BasicSimulation
    {
    private:
        PopulationPtr m_population;
        std::vector<SweepInterfacePtr> m_sweeps;
        std::vector<TimestepReporterInterfacePtr> m_timestepReporters;
        

    public:
        /**
         * @brief Construct a new Basic Simulation object
         * 
         * @param population Population simulation should work on
         */
        BasicSimulation(PopulationPtr population);
        ~BasicSimulation() = default;

        /**
         * @brief Add a sweep to the population
         * Sweeps sholud be added in the order they will be run each iteration
         * @param sweep Sweep to add
         */
        void addSweep(SweepInterfacePtr sweep);

        /**
         * @brief Attach a reporter to the simulation
         * Timestep Reporter to output information iteration steps
         * @param reporter Timestep Reporter to add
         */
        void addTimestepReporter(TimestepReporterInterfacePtr reporter);

        /**
         * @brief Perform Simulation
         * Run the configured simulation
         * @param timesteps Number of timesteps ot run for
         */
        void simulate(unsigned short timesteps);

    private:
        void setup();
        void teardown();
    };

    typedef std::shared_ptr<BasicSimulation> BasicSimulationPtr;

}


#endif // EPIABM_SIMULATINS_BASIC_SIMULATION_HPP

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
        BasicSimulation(PopulationPtr population);
        ~BasicSimulation();

        void addSweep(SweepInterfacePtr sweep);

        void addTimestepReporter(TimestepReporterInterfacePtr reporter);

        void simulate(unsigned short timesteps);

    private:
        void setup();
        void teardown();
    };

    typedef std::shared_ptr<BasicSimulation> BasicSimulationPtr;

}


#endif // EPIABM_SIMULATIONS_BASIC_SIMULATION_HPP

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
     * @brief Class to setup simulation closely matching Covid-Sim
     * 
     */
    class CovidSim
    {
    private:
        PopulationPtr m_population;
        std::vector<SweepInterfacePtr> m_sweeps;
        std::vector<TimestepReporterInterfacePtr> m_timestepReporters;
        

    public:
        CovidSim(PopulationPtr population);
        ~CovidSim() = default;

        void addSweep(SweepInterfacePtr sweep);

        void addTimestepReporter(TimestepReporterInterfacePtr reporter);

        void simulate(unsigned short timesteps);

    private:
        void setup();
        void teardown();
    };

    typedef std::shared_ptr<BasicSimulation> BasicSimulationPtr;

}


#endif // EPIABM_SIMULATINS_BASIC_SIMULATION_HPP

#ifndef EPIABM_SIMULATINS_Threaded_SIMULATION_HPP
#define EPIABM_SIMULATINS_Threaded_SIMULATION_HPP


#include "../sweeps/sweep_interface.hpp"
#include "../reporters/timestep_reporter_interface.hpp"

#include "../dataclasses/population.hpp"
#include "../utilities/thread_pool.hpp"

#include <memory>
#include <vector>


namespace epiabm
{

    class ThreadedSimulation
    {
    private:
        PopulationPtr m_population;
        std::map<size_t, std::vector<SweepInterfacePtr>> m_sweeps;
        std::vector<TimestepReporterInterfacePtr> m_timestepReporters;
        
        thread_pool m_pool;

    public:
        ThreadedSimulation(PopulationPtr population, std::optional<size_t> nThreads);
        ~ThreadedSimulation() = default;

        void addSweep(SweepInterfacePtr sweep, size_t group);

        void addTimestepReporter(TimestepReporterInterfacePtr reporter);

        void simulate(unsigned short timesteps);

    private:
        void setup();
        void teardown();
    };

    typedef std::shared_ptr<ThreadedSimulation> ThreadedSimulationPtr;

}


#endif // EPIABM_SIMULATINS_BASIC_SIMULATION_HPP

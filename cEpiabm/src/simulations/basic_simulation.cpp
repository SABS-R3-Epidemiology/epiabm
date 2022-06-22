
#include "basic_simulation.hpp"

#include "../logfile.hpp"

#include <chrono>

namespace epiabm
{

    BasicSimulation::BasicSimulation(PopulationPtr population) :
        m_population(population),
        m_sweeps(),
        m_timestepReporters()
    {
    }

    void BasicSimulation::addSweep(SweepInterfacePtr sweep)
    {
        m_sweeps.push_back(sweep);
    }

    void BasicSimulation::addTimestepReporter(TimestepReporterInterfacePtr timestepReporter)
    {
        m_timestepReporters.push_back(timestepReporter);
    }

    void BasicSimulation::simulate(const unsigned short timesteps)
    {
        auto t0 = std::chrono::system_clock::now();
        LOG << LOG_LEVEL_NORMAL << "Setting up Simulation.";
        setup();

        LOG << LOG_LEVEL_NORMAL << "Iterating through timesteps...";
        //try
        //{
            for (const auto& reporter : m_timestepReporters)
                    reporter->report(m_population, 0);

            for (unsigned short timestep = 1; timestep <= timesteps; timestep++)
            {
                // Run Sweeps
                for (const auto& sweep : m_sweeps) (*sweep)(timestep);

                // Report
                for (const auto& reporter : m_timestepReporters)
                    reporter->report(m_population, timestep);
            }
        //}
        // LCOV_EXCL_START
        /*
        catch (std::exception& e)
        {
            LOG << LOG_LEVEL_ERROR << "Error iterating through timesteps: " << e.what();
        }*/
        // LCOV_EXCL_STOP
        LOG << LOG_LEVEL_NORMAL << "Completed Iterating through timesteps.";

        teardown();
        
        // Log Simulation Run Time
        int64_t seconds = std::chrono::duration_cast<std::chrono::seconds>(
            std::chrono::system_clock::now() - t0).count();
        LOG << LOG_LEVEL_NORMAL << "Simulation Completed in "
            << seconds / 60 << "m " << seconds % 60 << "s";
    }

    void BasicSimulation::setup()
    {
        m_population->initialize();

        // Bind populations
        for (const auto& sweep : m_sweeps) sweep->bind_population(m_population);

        // Setup reporters
        for (const auto& reporter : m_timestepReporters) reporter->setup(m_population);
    }

    void BasicSimulation::teardown()
    {
        LOG << LOG_LEVEL_NORMAL << "Running Simulation Teardown.";

        // Teardown Reporters
        for (const auto& reporter : m_timestepReporters) reporter->teardown();
    }


} // namespace epiabm


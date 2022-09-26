
#include "threaded_simulation.hpp"

#include "../logfile.hpp"

#include <chrono>

namespace epiabm
{

    /**
     * @brief Construct a new Threaded Simulation:: Threaded Simulation object
     * 
     * @param population Population simulation should work on
     * @param nThreads Number of threads to run simulation across
     */
    ThreadedSimulation::ThreadedSimulation(PopulationPtr population, std::optional<size_t> nThreads) :
        m_population(population),
        m_sweeps(),
        m_timestepReporters(),
        m_pool(nThreads.value_or(std::thread::hardware_concurrency()))
    {
    }

    /**
     * @brief Destroy the Threaded Simulation:: Threaded Simulation object
     * 
     */
    ThreadedSimulation::~ThreadedSimulation() = default;

    /**
     * @brief Add a sweep to the population
     * Sweeps sholud be added in the order they will be run each iteration
     * Sweeps are run in groups. Within a group the sweeps are distributed amongst the cells across threads and so order is not guaranteed.
     * Sweep groups are guaranteed to run in order.
     * @param sweep Sweep to add
     * @param group Sweep group number to add sweep to
     */
    void ThreadedSimulation::addSweep(SweepInterfacePtr sweep, size_t group)
    {
        m_sweeps[group].push_back(sweep);
    }

    /**
     * @brief Attach a reporter to the simulation
     * Timestep Reporter to output information iteration steps
     * @param reporter Timestep Reporter to add
     */
    void ThreadedSimulation::addTimestepReporter(TimestepReporterInterfacePtr timestepReporter)
    {
        m_timestepReporters.push_back(timestepReporter);
    }

    /**
     * @brief Perform Simulation
     * Run the configured simulation
     * @param timesteps Number of timesteps ot run for
     */
    void ThreadedSimulation::simulate(const unsigned short timesteps)
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
                for (const auto& sweepGroup : m_sweeps)
                {
                    LOG << LOG_LEVEL_DEBUG << "Performing Sweep Group " << sweepGroup.first << " at timestep " << timestep;
                    m_population->forEachCell(
                        [this,timestep,&sweepGroup](Cell* cell)
                        {
                            m_pool.push_task(
                            [cell,timestep,&sweepGroup]()
                            {
                                for (const auto& sweep : sweepGroup.second)
                                    sweep->cellCallback(timestep, cell);
                                }
                            );
                            return true;
                        });
                    LOG << LOG_LEVEL_DEBUG << m_pool.get_tasks_total() << " unfinished tasks";
                    m_pool.wait_for_tasks();
                }

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
        // LCOV_EXCL_END
        LOG << LOG_LEVEL_NORMAL << "Completed Iterating through timesteps.";

        teardown();
        
        // Log Simulation Run Time
        int64_t seconds = std::chrono::duration_cast<std::chrono::seconds>(
            std::chrono::system_clock::now() - t0).count();
        LOG << LOG_LEVEL_NORMAL << "Simulation Completed in "
            << seconds / 60 << "m " << seconds % 60 << "s";
    }

    void ThreadedSimulation::setup()
    {
        LOG << LOG_LEVEL_NORMAL << "Threaded Simulation with " << m_pool.get_thread_count() << " threads.";
        m_population->initialize();

        // Bind populations
        for (const auto& sweepGroup : m_sweeps)
            for (const auto& sweep : sweepGroup.second) sweep->bind_population(m_population);

        // Setup reporters
        for (const auto& reporter : m_timestepReporters) reporter->setup(m_population);
    }

    void ThreadedSimulation::teardown()
    {
        LOG << LOG_LEVEL_NORMAL << "Running Simulation Teardown.";

        // Teardown Reporters
        for (const auto& reporter : m_timestepReporters) reporter->teardown();
    }


} // namespace epiabm


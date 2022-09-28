
#include "new_cases_reporter.hpp"
#include "../logfile.hpp"


namespace epiabm
{

    /**
     * @brief Construct a new Per Cell Compartment Reporter object
     * 
     * @param folder Folder to output to
     */
    NewCasesReporter::NewCasesReporter(const std::string file) :
        TimestepReporterInterface(std::filesystem::path(file).parent_path(), false)
    {
        m_os = m_folder.OpenOutputFile(std::filesystem::path(file).filename());
    }

    /**
     * @brief Destroy the Per Cell Compartment Reporter:: Per Cell Compartment Reporter object
     * 
     */
    NewCasesReporter::~NewCasesReporter() = default;

    /**
     * @brief Setup method which is called immediately before iterations begin
     * 
     * @param pop Initialized population before the iterations start
     */
    void NewCasesReporter::setup(PopulationPtr /*population*/)
    {
        *m_os << "timestep,new_cases" << std::endl;
    }

    /**
     * @brief Report the population state at a timestep
     * 
     * @param pop Population to report
     * @param timestep Timestep of report
     */
    void NewCasesReporter::report(
        const PopulationPtr population,
        const unsigned short timestep)
    {
        try
        {
            unsigned int new_cases = 0;
            population->forEachCell(
                [&new_cases, timestep](Cell* cell)
                {
                    cell->forEachPerson([&new_cases, timestep](Person* person)
                    {
                        if (person->params().infection_start_timestep > (timestep-1) &&
                            person->status() != InfectionStatus::Susceptible)
                            new_cases += 1;
                        return true;
                    });
                    return true;
                });
            *m_os << timestep << "," << new_cases << std::endl;
        }
        // LCOV_EXCL_START
        catch (std::exception& e)
        {
            LOG << LOG_LEVEL_ERROR << "Per-Cell Compartment Reporter Error writing to file";
            throw e;
        }
        // LCOV_EXCL_STOP
    }

    /**
     * @brief Clean up method
     * Called after the simulation has completed to finalise the output files
     */
    void NewCasesReporter::teardown()
    {
        *m_os << std::flush;
        m_os->close();
    }

} // namespace epiabm


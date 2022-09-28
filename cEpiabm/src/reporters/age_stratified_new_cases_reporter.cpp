
#include "age_stratified_new_cases_reporter.hpp"
#include "../logfile.hpp"


namespace epiabm
{

    /**
     * @brief Construct a new Per Cell Compartment Reporter object
     * 
     * @param folder Folder to output to
     */
    AgeStratifiedNewCasesReporter::AgeStratifiedNewCasesReporter(const std::string file) :
        TimestepReporterInterface(std::filesystem::path(file).parent_path(), false)
    {
        m_os = m_folder.OpenOutputFile(std::filesystem::path(file).filename());
    }

    /**
     * @brief Destroy the Per Cell Compartment Reporter:: Per Cell Compartment Reporter object
     * 
     */
    AgeStratifiedNewCasesReporter::~AgeStratifiedNewCasesReporter() = default;

    /**
     * @brief Setup method which is called immediately before iterations begin
     * 
     * @param pop Initialized population before the iterations start
     */
    void AgeStratifiedNewCasesReporter::setup(PopulationPtr /*population*/)
    {
        *m_os << "timestep,age_group,new_cases" << std::endl;
    }

    /**
     * @brief Report the population state at a timestep
     * 
     * @param pop Population to report
     * @param timestep Timestep of report
     */
    void AgeStratifiedNewCasesReporter::report(
        const PopulationPtr population,
        const unsigned short timestep)
    {
        try
        {
            std::map<unsigned char, unsigned int> new_cases;
            population->forEachCell(
                [&new_cases, timestep](Cell* cell)
                {
                    cell->forEachPerson([&new_cases, timestep](Person* person)
                    {
                        if (person->params().infection_start_timestep > (timestep-1) &&
                            person->status() != InfectionStatus::Susceptible)
                            new_cases[person->params().age_group] += 1;
                        return true;
                    });
                    return true;
                });
            for (const auto& p : new_cases)
                *m_os << timestep << "," << static_cast<unsigned int>(p.first) << "," << p.second << std::endl;
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
    void AgeStratifiedNewCasesReporter::teardown()
    {
        *m_os << std::flush;
        m_os->close();
    }

} // namespace epiabm


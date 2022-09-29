
#include "age_stratified_population_reporter.hpp"
#include "../logfile.hpp"


namespace epiabm
{

    /**
     * @brief Construct a new Population Compartment Reporter object
     * If the file already exists, it will be overwritten
     * @param file File to write to
     */
    AgeStratifiedPopulationReporter::AgeStratifiedPopulationReporter(const std::string file) :
        TimestepReporterInterface(std::filesystem::path(file).parent_path(), false),
        m_compartments(
            {
            InfectionStatus::Susceptible,
            InfectionStatus::Exposed,
            InfectionStatus::InfectASympt,
            InfectionStatus::InfectMild,
            InfectionStatus::InfectGP,
            InfectionStatus::InfectHosp,
            InfectionStatus::InfectICU,
            InfectionStatus::InfectICURecov,
            InfectionStatus::Dead,
            InfectionStatus::Recovered
            })
    {
        m_os = m_folder.OpenOutputFile(std::filesystem::path(file).filename());
    }

    /**
     * @brief Construct a new Population Compartment Reporter object
     * If the file already exists, it will be overwritten
     * @param file File to write to
     */
    AgeStratifiedPopulationReporter::~AgeStratifiedPopulationReporter() = default;

    /**
     * @brief Setup method which is called immediately before iterations begin
     *
     * @param pop Initialized population before the iterations start
     */
    void AgeStratifiedPopulationReporter::setup(PopulationPtr /*population*/)
    {
        *m_os << "timestep,age_group";
        for (const InfectionStatus status : m_compartments)
        {
            *m_os << "," << status_string(status);
        }
        *m_os << std::endl;
    }

    /**
     * @brief Report the population state at a timestep
     *
     * @param pop Population to report
     * @param timestep Timestep of report
     */
    void AgeStratifiedPopulationReporter::report(
        const PopulationPtr population,
        const unsigned short timestep)
    {
        try
        {

            std::map<unsigned char, std::map<InfectionStatus, unsigned int>> statusCount;
            population->forEachCell(
                [&statusCount](Cell* cell)
                {
                    cell->forEachPerson(
                    [&statusCount](Person* p)
                    {
                        statusCount[p->params().age_group][p->status()] += 1;
                        return true;
                    });
                    return true;
                });

            for (const auto& age : statusCount)
            {
                *m_os << timestep << ","
                    << static_cast<unsigned int>(age.first);
                for (const auto& c : m_compartments)
                {
                    *m_os << "," << statusCount[age.first][c];
                }
                *m_os << std::endl;
            }

        }
        // LCOV_EXCL_START
        catch (std::exception& e)
        {
            LOG << LOG_LEVEL_ERROR << "Cell Compartment Reporter Error writing to file";
            throw e;
        }
        // LCOV_EXCL_STOP
    }

    /**
     * @brief Getter for set which contains the compartment types to return
     * This set can be configured to specify which compartments to output
     * @return std::set<InfectionStatus>&
     */
    std::set<InfectionStatus>& AgeStratifiedPopulationReporter::compartments()
    {
        return m_compartments;
    }

} // namespace epiabm


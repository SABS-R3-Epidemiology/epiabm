
#include "population_compartment_reporter.hpp"
#include "../logfile.hpp"


namespace epiabm
{

    /**
     * @brief Construct a new Population Compartment Reporter object
     * If the file already exists, it will be overwritten
     * @param file File to write to
     */
    PopulationCompartmentReporter::PopulationCompartmentReporter(const std::string file) :
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
    PopulationCompartmentReporter::~PopulationCompartmentReporter() = default;

    /**
     * @brief Setup method which is called immediately before iterations begin
     *
     * @param pop Initialized population before the iterations start
     */
    void PopulationCompartmentReporter::setup(PopulationPtr /*population*/)
    {
        *m_os << "timestep";
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
    void PopulationCompartmentReporter::report(
        const PopulationPtr population,
        const unsigned short timestep)
    {
        try
        {
            *m_os << timestep;

            std::map<InfectionStatus, unsigned int> statusCount;
            population->forEachCell(
                [this, &statusCount](Cell* cell)
                {
                    for (const auto& c : m_compartments)
                    {
                        statusCount[c] += cell->compartmentCount(c);
                    }
                    return true;
                });

            for (const auto& c : m_compartments)
            {
                *m_os << "," << statusCount[c];
            }
            *m_os << std::endl;

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
    std::set<InfectionStatus>& PopulationCompartmentReporter::compartments()
    {
        return m_compartments;
    }

} // namespace epiabm


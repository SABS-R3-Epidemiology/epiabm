
#include "cell_compartment_reporter.hpp"
#include "../logfile.hpp"


namespace epiabm
{

    /**
     * @brief Construct a new Cell Compartment Reporter object
     * 
     * @param folder Output Folder
     */
    CellCompartmentReporter::CellCompartmentReporter(const std::string folder) :
        TimestepReporterInterface(folder, true),
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
    {}

    /**
     * @brief Destroy the Cell Compartment Reporter:: Cell Compartment Reporter object
     * 
     */
    CellCompartmentReporter::~CellCompartmentReporter() = default;

    /**
     * @brief Report the population state at a timestep
     * 
     * @param pop Population to report
     * @param timestep Timestep of report
     */
    void CellCompartmentReporter::report(
        const PopulationPtr population,
        const unsigned short timestep)
    {
        ofstreamPtr ofs = m_folder.OpenOutputFile(
            "results_timestep_" + std::to_string(timestep));
        try
        {
            *ofs << "CellIndex";
            std::for_each(m_compartments.begin(), m_compartments.end(),
                [&ofs](const InfectionStatus status)
                {
                    *ofs << "," << status_string(status);
                });
            *ofs << std::endl;

            population->forEachCell(
                [&ofs, this](Cell* cell)
                {
                    *ofs << cell->index();
                    std::for_each(m_compartments.begin(), m_compartments.end(),
                        [ofs, cell](const InfectionStatus status)
                        {
                            *ofs << "," << cell->compartmentCount(status);
                        });
                    *ofs << std::endl;
                    return true;
                });
        }
        // LCOV_EXCL_START
        catch (std::exception& e)
        {
            LOG << LOG_LEVEL_ERROR << "Cell Compartment Reporter Error writing to file";
            throw e;
        }
        // LCOV_EXCL_STOP
        ofs->close();
    }

    /**
     * @brief Getter for set which contains the compartment types to return
     * This set can be configured to specify which compartments to output
     * @return std::set<InfectionStatus>& 
     */
    std::set<InfectionStatus>& CellCompartmentReporter::compartments()
    {
        return m_compartments;
    }

} // namespace epiabm


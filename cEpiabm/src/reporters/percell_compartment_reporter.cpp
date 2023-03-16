
#include "percell_compartment_reporter.hpp"
#include "../logfile.hpp"


namespace epiabm
{

    /**
     * @brief Construct a new Per Cell Compartment Reporter object
     * 
     * @param folder Folder to output to
     */
    PerCellCompartmentReporter::PerCellCompartmentReporter(const std::string folder) :
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
            }),
        m_cellFileMap()
    {}

    /**
     * @brief Destroy the Per Cell Compartment Reporter:: Per Cell Compartment Reporter object
     * 
     */
    PerCellCompartmentReporter::~PerCellCompartmentReporter() = default;

    /**
     * @brief Setup method which is called immediately before iterations begin
     * 
     * @param pop Initialized population before the iterations start
     */
    void PerCellCompartmentReporter::setup(PopulationPtr population)
    {
        teardown(); // Close all open files if exist, and clear cell file map
        // Create cell file map
        population->forEachCell(
            [this](Cell* cell)
            {
                m_cellFileMap[cell->index()] = m_folder.OpenOutputFile("results_cell_" + std::to_string(cell->index()));
                *m_cellFileMap[cell->index()] << "timestep";
                for (const InfectionStatus status : m_compartments)
                {
                    *m_cellFileMap[cell->index()] << "," << status_string(status);
                }
                *m_cellFileMap[cell->index()] << std::endl;
                return true;
            });
    }

    /**
     * @brief Report the population state at a timestep
     * 
     * @param pop Population to report
     * @param timestep Timestep of report
     */
    void PerCellCompartmentReporter::report(
        const PopulationPtr population,
        const unsigned short timestep)
    {
        try
        {
            population->forEachCell(
                [this, timestep](Cell* cell)
                {
                    *m_cellFileMap[cell->index()] << timestep;
                    for (const InfectionStatus status : m_compartments)
                    {
                        *m_cellFileMap[cell->index()] << "," << cell->compartmentCount(status);
                    }
                    *m_cellFileMap[cell->index()] << std::endl;
                    return true;
                });
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
    void PerCellCompartmentReporter::teardown()
    {
        for (const auto& p : m_cellFileMap)
        {
            p.second->close();
        }
        m_cellFileMap.clear();
    }

    /**
     * @brief Getter for set which contains the compartment types to return
     * This set can be configured to specify which compartments to output
     * @return std::set<InfectionStatus>& 
     */
    std::set<InfectionStatus>& PerCellCompartmentReporter::compartments()
    {
        return m_compartments;
    }

} // namespace epiabm


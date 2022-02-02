
#include "percell_compartment_reporter.hpp"
#include "../logfile.hpp"


namespace epiabm
{


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
        // LCOV_EXCL_END
    }

    void PerCellCompartmentReporter::teardown()
    {
        for (const auto& p : m_cellFileMap)
        {
            p.second->close();
        }
        m_cellFileMap.clear();
    }

    std::set<InfectionStatus>& PerCellCompartmentReporter::compartments()
    {
        return m_compartments;
    }

} // namespace epiabm


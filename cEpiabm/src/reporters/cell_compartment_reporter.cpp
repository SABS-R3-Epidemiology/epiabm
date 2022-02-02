
#include "cell_compartment_reporter.hpp"
#include "../logfile.hpp"


namespace epiabm
{


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
        // LCOV_EXCL_END
        ofs->close();
    }

    std::set<InfectionStatus>& CellCompartmentReporter::compartments()
    {
        return m_compartments;
    }

} // namespace epiabm


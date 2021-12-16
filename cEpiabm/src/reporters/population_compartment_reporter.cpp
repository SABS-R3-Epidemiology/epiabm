
#include "population_compartment_reporter.hpp"
#include "../logfile.hpp"


namespace epiabm
{


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

    void PopulationCompartmentReporter::setup(PopulationPtr /*population*/)
    {
        *m_os << "timestep";
        for (const InfectionStatus status : m_compartments)
        {
            *m_os << "," << status_string(status);
        }
        *m_os << std::endl;
    }

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
        catch (std::exception& e)
        {
            LOG << LOG_LEVEL_ERROR << "Cell Compartment Reporter Error writing to file";
            throw e;
        }
    }

    std::set<InfectionStatus>& PopulationCompartmentReporter::compartments()
    {
        return m_compartments;
    }

} // namespace epiabm


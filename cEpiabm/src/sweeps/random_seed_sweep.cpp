
#include "random_seed_sweep.hpp"
#include "../logfile.hpp"

namespace epiabm
{


    RandomSeedSweep::RandomSeedSweep(SimulationConfigPtr simulationConfig, int per_n_people) :
        SweepInterface(simulationConfig),
        m_infectRate(per_n_people),
        m_infected(0)
    {}

    void RandomSeedSweep::operator()(const unsigned short timestep)
    {
        m_infected = 0;
        m_population->forEachCell(std::bind(
            &RandomSeedSweep::cellCallback, this,
            timestep, std::placeholders::_1));
        LOG << LOG_LEVEL_INFO << "Randomly seeded " << m_infected << " people at timestep " << timestep;
    }

    bool RandomSeedSweep::cellCallback(
        const unsigned short timestep,
        Cell* cell)
    {
        cell->forEachPerson(std::bind(
            &RandomSeedSweep::cellPersonCallback, this,
            timestep, cell, std::placeholders::_1));
        return true;
    }

    bool RandomSeedSweep::cellPersonCallback(
        unsigned short timestep,
        Cell* cell,
        Person* person)
    {
        if (m_cfg->randomManager->g().randi<int>(INT32_MAX)%m_infectRate < 1)
        {
            person->updateStatus(cell, InfectionStatus::Exposed, timestep);
            person->params().next_status_time = static_cast<unsigned short>(timestep);
            cell->markExposed(person->cellPos());
            m_infected++;
        }
        return true;
    }
}



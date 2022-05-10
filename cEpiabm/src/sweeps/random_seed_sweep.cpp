
#include "random_seed_sweep.hpp"


namespace epiabm
{


    RandomSeedSweep::RandomSeedSweep(int per_n_people) :
        m_infectRate(per_n_people)
    {}

    void RandomSeedSweep::operator()(const unsigned short timestep)
    {
        m_population->forEachCell(std::bind(
            &RandomSeedSweep::cellCallback, this,
            timestep, std::placeholders::_1));
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
        if (rand()%m_infectRate < 1)
        {
            person->updateStatus(cell, InfectionStatus::Exposed, timestep);
            person->params().next_status_time = static_cast<unsigned short>(timestep + 10);
        }
        return true;
    }
}



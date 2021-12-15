
#include "basic_host_progression_sweep.hpp"


namespace epiabm
{

    BasicHostProgressionSweep::BasicHostProgressionSweep() {}

    void BasicHostProgressionSweep::operator()(const unsigned short timestep)
    {
        m_population->forEachCell(std::bind(
            &BasicHostProgressionSweep::cellCallback, this,
            timestep, std::placeholders::_1));
    }

    bool BasicHostProgressionSweep::cellCallback(
        const unsigned short timestep, Cell* cell)
    {
        cell->forEachInfectious(std::bind(
            &BasicHostProgressionSweep::cellInfectiousCallback, this,
            timestep, cell, std::placeholders::_1));
        cell->forEachExposed(std::bind(
            &BasicHostProgressionSweep::cellExposedCallback, this,
            timestep, cell, std::placeholders::_1));
        return true;
    }

    bool BasicHostProgressionSweep::cellExposedCallback(
        const unsigned short timestep,
        Cell* cell, Person* person)
    {
        if (timestep < person->params().next_status_time) return true;
        InfectionStatus next = first_infectious_status(person);
        person->updateStatus(next);
        person->params().next_status_time = time_to_next_status(person, next);
        cell->markInfectious(person->cellPos());
        return true;
    }

    bool BasicHostProgressionSweep::cellInfectiousCallback(
        const unsigned short timestep,
        Cell* cell, Person* person)
    {
        if (timestep < person->params().next_status_time) return true;
        InfectionStatus next = next_status(person);
        person->updateStatus(next);

        if (next == InfectionStatus::Recovered)
        {
            cell->markRecovered(person->cellPos());
            return true;
        }
        cell->markDead(person->cellPos());
        return true;
    }

    inline unsigned short BasicHostProgressionSweep::time_to_next_status(Person* /*person*/, InfectionStatus /*status*/)
    {
        return static_cast<unsigned short>(std::rand() % 10 + 1);
    }

    inline InfectionStatus BasicHostProgressionSweep::first_infectious_status(Person* person)
    {
        person->params().infectiousness = 1; // This should become age dependent infectiousness
        // Covidsim has modifier here to randomly reduce infectiousness
        return InfectionStatus::InfectASympt;        
    }

    inline InfectionStatus BasicHostProgressionSweep::next_status(Person* /*person*/)
    {
        double deathChance = 0.1; // This needs to become a parameter
        if (static_cast<double>(rand()%1000) / 1000.0 < deathChance)
        {
            return InfectionStatus::Dead;
        }
        else
        {
            return InfectionStatus::Recovered;
        }
    }

} // namespace epiabm


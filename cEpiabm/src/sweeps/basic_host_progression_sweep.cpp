
#include "basic_host_progression_sweep.hpp"
#include "../logfile.hpp"

namespace epiabm
{

    BasicHostProgressionSweep::BasicHostProgressionSweep(SimulationConfigPtr cfg) :
        SweepInterface(cfg)
    {}

    void BasicHostProgressionSweep::operator()(const unsigned short timestep)
    {
        LOG << LOG_LEVEL_DEBUG << "Beginning Basic Host Progression Sweep " << timestep;
        m_population->forEachCell(std::bind(
            &BasicHostProgressionSweep::cellCallback, this,
            timestep, std::placeholders::_1));
        LOG << LOG_LEVEL_DEBUG << "Finished Basic Host Progression Sweep " << timestep;
    }

    /**
     * @brief Cell callback
     * Process Infectious.
     * Process Exposed.
     * @param timestep 
     * @param cell 
     * @return true 
     * @return false 
     */
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

    /**
     * @brief Exposed Person Callback
     * Check if time to transition.
     * If should transition, move person from Exposed to next status (always InfectAsymp in this basic class)
     * Set time to remain in this state.
     * Also update the cell of status for fast looping through subsets of people.
     * @param timestep 
     * @param cell 
     * @param person 
     * @return true 
     * @return false 
     */
    bool BasicHostProgressionSweep::cellExposedCallback(
        const unsigned short timestep,
        Cell* cell, Person* person)
    {
        if (timestep < person->params().next_status_time) return true;
        InfectionStatus next = first_infectious_status(person);
        person->updateStatus(cell, next, timestep);
        person->params().next_status_time = time_to_next_status(person, next);
        cell->markInfectious(person->cellPos());
        return true;
    }

    /**
     * @brief Infectious person callback
     * In this class infectious person's status is always InfectAsymp
     * Check if time to transition has passed.
     * If should transition, decide person's next state. (In this basic class, this is always Dead or Recovered)
     * Update person's state. (Since always Dead or Recovered, no next state time)
     * Update cell of state change.
     * @param timestep 
     * @param cell 
     * @param person 
     * @return true 
     * @return false 
     */
    bool BasicHostProgressionSweep::cellInfectiousCallback(
        const unsigned short timestep,
        Cell* cell, Person* person)
    {
        if (timestep < person->params().next_status_time) return true;
        InfectionStatus next = next_status(person);
        LOG << LOG_LEVEL_INFO << "Basic host progression of ("
            << cell->index() << "," << person->cellPos() << ") from "
            << status_string(person->status()) << " to " << status_string(next);
        person->updateStatus(cell, next, timestep);

        if (next == InfectionStatus::Recovered)
        {
            cell->markRecovered(person->cellPos());
            return true;
        }
        cell->markDead(person->cellPos());
        return true;
    }

    /**
     * @brief Generate time to next state.
     * Depends on person, their previous state and the state they are moving to.
     */
    inline unsigned short BasicHostProgressionSweep::time_to_next_status(Person* /*person*/, InfectionStatus /*status*/)
    {
        return static_cast<unsigned short>(std::rand() % 14 + 14);
    }

    /**
     * @brief Choose first infected state.
     * Choose state for person to progress from Exposed with.
     * (In this basic class it is always InfectAsymp, but in future can be InfectMild, InfectGP).
     * @param person 
     * @return InfectionStatus 
     */
    inline InfectionStatus BasicHostProgressionSweep::first_infectious_status(Person* person)
    {
        person->params().infectiousness = 1; // This should become age dependent infectiousness
        // Covidsim has modifier here to randomly reduce infectiousness
        return InfectionStatus::InfectASympt;        
    }

    /**
     * @brief Choose next state once already infected.
     * Choose next state for person.
     * (In this basic class this can only be Recovered or Dead. In future, this will allow transitioning from InfectGP->InfectHosp->InfectICU->InfectICURecov)
     */
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


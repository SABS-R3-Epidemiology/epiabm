
#include "new_infection_sweep.hpp"
#include "../logfile.hpp"

namespace epiabm
{


    NewInfectionSweep::NewInfectionSweep(SimulationConfigPtr cfg) :
        SweepInterface(cfg),
        m_counter(0)
    {}


    void NewInfectionSweep::operator()(const unsigned short timestep)
    {
        LOG << LOG_LEVEL_DEBUG << "Beginning New Infection Sweep " << timestep;
        m_counter = 0;
        m_population->forEachCell(std::bind(
            &NewInfectionSweep::cellCallback, this,
            timestep, std::placeholders::_1));
        LOG << LOG_LEVEL_INFO << "New Infection Sweep " << timestep << " processed " << m_counter << " new infections.";
        LOG << LOG_LEVEL_DEBUG << "Finished New Infection Sweep " << timestep;
    }

    /**
     * @brief Callback for each cell
     * For each cell, process each person in the queue
     * @param timestep 
     * @param cell 
     * @return true 
     * @return false 
     */
    bool NewInfectionSweep::cellCallback(const unsigned short timestep, Cell* cell)
    {
        cell->processQueue(std::bind(
            &NewInfectionSweep::cellPersonQueueCallback, this,
            timestep, cell, std::placeholders::_1));
        return true;
    }

    /**
     * @brief Callback for each person in a cell's queue
     * Process the people queued to be infected.
     * Change status to Exposed, set the next transition time and mark the person as Exposed in the cell for fast looping through subsets of people.
     * @param timestep 
     * @param cell 
     * @param personIndex 
     */
    void NewInfectionSweep::cellPersonQueueCallback(unsigned short timestep, Cell* cell, size_t personIndex)
    {
        Person* person = &cell->getPerson(personIndex);
        {
            std::stringstream ss;
            ss << "New infection sweep on ("
                << cell->index() << "," << person->cellPos() << ")";
            LOG << LOG_LEVEL_DEBUG << ss.str();
        }
        person->updateStatus(cell, InfectionStatus::Exposed, timestep);
        person->params().next_status_time = static_cast<unsigned short>(timestep + latent_time(person));
        cell->markExposed(personIndex);
        m_counter++;
    }

    unsigned short NewInfectionSweep::latent_time(Person* /*person*/)
    {
        return m_cfg->infectionConfig->hostProgressionConfig->latentPeriodICDF.choose(
            m_cfg->timestepsPerDay, m_cfg->randomManager->g());
    }


} // namespace epiabm

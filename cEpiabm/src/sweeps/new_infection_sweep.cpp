
#include "new_infection_sweep.hpp"


namespace epiabm
{


    NewInfectionSweep::NewInfectionSweep() {}


    void NewInfectionSweep::operator()(const unsigned short timestep)
    {
        m_population->forEachCell(std::bind(
            &NewInfectionSweep::cellCallback, this,
            timestep, std::placeholders::_1));
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
        person->updateStatus(InfectionStatus::Exposed);
        person->params().next_status_time = static_cast<unsigned short>(timestep + latent_time(person));
        cell->markExposed(personIndex);
    }

    unsigned short NewInfectionSweep::latent_time(Person* /*person*/)
    {
        return static_cast<unsigned short>(std::rand() % 10 + 1);
    }


} // namespace epiabm

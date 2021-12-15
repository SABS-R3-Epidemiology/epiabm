
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

    bool NewInfectionSweep::cellCallback(const unsigned short timestep, Cell* cell)
    {
        cell->processQueue(std::bind(
            &NewInfectionSweep::cellPersonQueueCallback, this,
            timestep, cell, std::placeholders::_1));
        return true;
    }

    void NewInfectionSweep::cellPersonQueueCallback(const unsigned short /*timestep*/, Cell* cell, size_t personIndex)
    {
        cell->getPerson(personIndex).updateStatus(InfectionStatus::Exposed);
    }


} // namespace epiabm

#include "host_progression_sweep.hpp"
#include "../logfile.hpp"

#include <memory>

namespace epiabm
{

    HostProgressionSweep::HostProgressionSweep(SimulationConfigPtr cfg) : SweepInterface(cfg)
    {}

    void HostProgressionSweep::operator()(const unsigned short timestep)
    {
        LOG << LOG_LEVEL_DEBUG << "Beginning Host Progression Sweep " << timestep;
        m_population->forEachCell(std::bind(
            &HostProgressionSweep::cellCallback, this,
            timestep, std::placeholders::_1));
        LOG << LOG_LEVEL_DEBUG << "Finished Host Progression Sweep " << timestep;
    }

    bool HostProgressionSweep::cellCallback(
        const unsigned short timestep, Cell *cell)
    {
        cell->forEachInfectious(std::bind(
            &HostProgressionSweep::cellInfectiousCallback, this,
            timestep, cell, std::placeholders::_1));
        cell->forEachExposed(std::bind(
            &HostProgressionSweep::cellExposedCallback, this,
            timestep, cell, std::placeholders::_1));
        return true;
    }

    bool HostProgressionSweep::cellExposedCallback(
        const unsigned short timestep, Cell *cell, Person *person)
    {
    }

    bool HostProgressionSweep::cellInfectiousCallback(
        const unsigned short timestep, Cell *cell, Person *person)
    {
    }
} // namespace epiabm

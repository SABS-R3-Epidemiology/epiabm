
#include "sweep_interface.hpp"

namespace epiabm
{
    SweepInterface::SweepInterface() {}
    SweepInterface::SweepInterface(SimulationConfigPtr cfg) :
        m_cfg(cfg)
    {}

    void SweepInterface::bind_population(PopulationPtr population)
    {
        m_population = population;
    }

} // namespace epiabm

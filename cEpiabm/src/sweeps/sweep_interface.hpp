#ifndef EPIABM_SWEEPS_SWEEP_INTERFACE_HPP
#define EPIABM_SWEEPS_SWEEP_INTERFACE_HPP

#include "../dataclasses/population.hpp"

#include <memory>


namespace epiabm
{


    class SweepInterface
    {
    protected:
        PopulationPtr m_population;

    public:
        virtual ~SweepInterface() = default;

        void bind_population(PopulationPtr population);
        
        virtual void operator()(const unsigned short timestep) = 0;


    }; // class SweepInterface

    typedef std::shared_ptr<SweepInterface> SweepInterfacePtr;

} // namespace epiabm


#endif // EPIABM_SWEEPS_SWEEP_INTERFACE_HPP
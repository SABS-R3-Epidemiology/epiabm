#ifndef EPIABM_SWEEPS_SWEEP_INTERFACE_HPP
#define EPIABM_SWEEPS_SWEEP_INTERFACE_HPP

#include "../dataclasses/population.hpp"

#include <memory>


namespace epiabm
{

    /**
     * @brief Interface class for sweeps
     * Sweeps can have population bound, and then operate upon the bound populations each timestep.
     */
    class SweepInterface
    {
    protected:
        PopulationPtr m_population;

    public:
        SweepInterface(){};
        virtual ~SweepInterface() = default;

        /**
         * @brief Bind Population
         * Attach population to the sweep
         * @param population 
         */
        void bind_population(PopulationPtr population);
        
        /**
         * @brief Apply sweep
         * Act on the population. Called by Simulation class each iteration timestep.
         */
        virtual void operator()(const unsigned short /*timestep*/){};


    }; // class SweepInterface

    typedef std::shared_ptr<SweepInterface> SweepInterfacePtr;

} // namespace epiabm


#endif // EPIABM_SWEEPS_SWEEP_INTERFACE_HPP
#ifndef EPIABM_SWEEPS_SWEEP_INTERFACE_HPP
#define EPIABM_SWEEPS_SWEEP_INTERFACE_HPP

#include "../dataclasses/population.hpp"
#include "../configuration/simulation_config.hpp"

#include <memory>
#include <optional>

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
        SimulationConfigPtr m_cfg;

    public:
        SweepInterface();
        SweepInterface(SimulationConfigPtr cfg);
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

        /**
         * @brief Callback to apply sweep to each cell
         * 
         * @param timestep Current Timestep
         * @param cell Cell to act on
         * @return true Returns true to continue and callback on next cell
         * @return false Terminate Callbacks
         */
        virtual bool cellCallback(
            const unsigned short /*timestep*/,
            Cell* /*cell*/) { return true; }


    }; // class SweepInterface

    typedef std::shared_ptr<SweepInterface> SweepInterfacePtr;

} // namespace epiabm


#endif // EPIABM_SWEEPS_SWEEP_INTERFACE_HPP
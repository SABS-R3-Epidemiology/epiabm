#ifndef EPIABM_CONFIGURATION_SIMULATION_CONFIGURATION_HPP
#define EPIABM_CONFIGURATION_SIMULATION_CONFIGURATION_HPP

#include "infection_config.hpp"
#include "population_config.hpp"
#include "../utilities/random_manager.hpp"

#include <memory>
#include <filesystem>

namespace epiabm
{

    /**
     * @brief Highest level master configuration class
     * 
     * Class to contain configuration information on entire simulation.
     */
    class SimulationConfig
    {
    private:
    public:
        InfectionConfigPtr infectionConfig;
        PopulationConfigPtr populationConfig;

        unsigned short timestepsPerDay;
        RandomManagerPtr randomManager;

        /**
         * @brief Construct a new Simulation Config object
         * 
         */
        SimulationConfig()
        {
            infectionConfig = std::make_shared<InfectionConfig>();
            populationConfig = std::make_shared<PopulationConfig>();
            randomManager = std::make_shared<RandomManager>(0);
        }

    private:
    };

    typedef std::shared_ptr<SimulationConfig> SimulationConfigPtr;

} // epiabm

#endif // EPIABM_CONFIGURATION_SIMULATION_CONFIGURATION_HPP

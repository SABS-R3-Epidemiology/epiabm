#ifndef EPIABM_CONFIGURATION_JSON_CONFIGURATION_HELPER_HPP
#define EPIABM_CONFIGURATION_JSON_CONFIGURATION_HELPER_HPP

#include "json.hpp"
#include "simulation_config.hpp"

#include <memory>
#include <filesystem>

namespace epiabm
{

    /**
     * @brief Interface class for configuration factories
     * 
     * Factory pattern for configuration classes
     * Must have loadConfig method which takes a filepath input and returns a SimulationConfig class
     */
    class ConfigurationFactoryInterface
    {
    private:
    public:
        /**
         * @brief Construct a new Configuration Factory Interface object
         * 
         */
        ConfigurationFactoryInterface() {};
        /**
         * @brief Destroy the Configuration Factory Interface object
         * 
         */
        virtual ~ConfigurationFactoryInterface() = default;

        /**
         * @brief Load Config from File
         * 
         * Reads input file and creates SimulationConfig object
         */
        virtual SimulationConfigPtr loadConfig(
            const std::filesystem::path& /*configFile*/){ return std::shared_ptr<SimulationConfig>(); };

    protected:
    };

    typedef std::shared_ptr<ConfigurationFactoryInterface> ConfigurationFactoryPtr;

}

#endif // EPIABM_CONFIGURATION_JSON_CONFIGURATION_HELPER_HPP
#ifndef EPIABM_CONFIGURATION_JSON_CONFIGURATION_HELPER_HPP
#define EPIABM_CONFIGURATION_JSON_CONFIGURATION_HELPER_HPP

#include "json.hpp"
#include "simulation_config.hpp"

#include <memory>
#include <filesystem>

namespace epiabm
{

    class ConfigurationFactoryInterface
    {
    private:
    public:
        ConfigurationFactoryInterface() {};
        virtual ~ConfigurationFactoryInterface() = default;

        virtual SimulationConfigPtr loadConfig(
            const std::filesystem::path& /*configFile*/){ return std::shared_ptr<SimulationConfig>(); };

    protected:
    };

    typedef std::shared_ptr<ConfigurationFactoryInterface> ConfigurationFactoryPtr;

}

#endif // EPIABM_CONFIGURATION_JSON_CONFIGURATION_HELPER_HPP
#ifndef EPIABM_CONFIGURATION_JSON_FACTORY_HPP
#define EPIABM_CONFIGURATION_JSON_FACTORY_HPP

#include "config_factory_interface.hpp"
#include "simulation_config.hpp"
#include "../utilities/inverse_cdf.hpp"
#include "json.hpp"

#include <filesystem>

namespace json = nlohmann;

namespace epiabm
{

    /**
     * @brief Configuration Factory implementation which reads a json file into a SimulationConfig object
     * 
     */
    class JsonFactory : public ConfigurationFactoryInterface
    {
        private:
        public:
            JsonFactory();
            ~JsonFactory() = default;

            SimulationConfigPtr loadConfig(const json::json& input);
            SimulationConfigPtr loadConfig(
                const std::filesystem::path& configFile) override;

        private:
            void loadSimulationConfig(
                SimulationConfigPtr cfg,
                const json::json& input);

            bool loadPopulationConfig(
                PopulationConfigPtr cfg,
                const json::json& input);

            bool loadInfectionConfig(
                InfectionConfigPtr cfg,
                const json::json& j);
            
            bool loadTransitionTimeConfig(
                HostProgressionConfigPtr cfg,
                const json::json& j);

            bool loadTransitionStateConfig(
                HostProgressionConfigPtr cfg,
                const json::json& j);

            bool loadHostProgressionConfig(
                HostProgressionConfigPtr cfg,
                const json::json& j);

            template <typename T>
            const T retrieve(const json::json& j, const std::string& paramName);

            template <typename T>
            const T retrieve(const json::json& j, const std::string& paramName, const T& def);

            InverseCDF retrieveICDF(
                const json::json& j,
                const std::string& meanParamName,
                const std::string& icdfParamName); 

    };

    typedef std::shared_ptr<JsonFactory> JsonFactoryPtr;


} // namespace epiabm


#endif // EPIABM_CONFIGURATION_JSON_FACTORY_HPP
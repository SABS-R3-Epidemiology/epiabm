#include "json_factory.hpp"
#include "../logfile.hpp"

#include <iostream>
#include <fstream>

namespace epiabm
{

    /**
     * @brief Construct a new Json Factory:: Json Factory object
     * 
     */
    JsonFactory::JsonFactory() :
        ConfigurationFactoryInterface()
    {}

    /**
     * @brief Read Json into SimulationConfig
     * 
     * @param input input json object
     * @return SimulationConfigPtr Simulation Config object created from json input 
     */
    SimulationConfigPtr JsonFactory::loadConfig(const json::json& input)
    {
        SimulationConfigPtr config = std::make_shared<SimulationConfig>();
        loadSimulationConfig(config, input);
        if (!(
                loadInfectionConfig(config->infectionConfig, input) &&
                loadPopulationConfig(config->populationConfig, input) &&
                loadHostProgressionConfig(config->infectionConfig->hostProgressionConfig, input)))
            throw std::runtime_error("Json Factory Error Loading Config Files");
        return config;
    }

    /**
     * @brief Read Json file into SimulationConfig
     * 
     * @param configFile Input json filename
     * @return SimulationConfigPtr Simulation config object created from json file input
     */
    SimulationConfigPtr JsonFactory::loadConfig(const std::filesystem::path &configFile)
    {
        std::ifstream ifs(configFile);
        json::json input;
        ifs >> input;
        return loadConfig(input);
    }

    void JsonFactory::loadSimulationConfig(
        SimulationConfigPtr cfg, const json::json &j)
    {
        cfg->timestepsPerDay = retrieve<unsigned short>(j, "timesteps_per_day", 1);
        cfg->randomManager = std::make_shared<RandomManager>(
            retrieve<unsigned int>(j, "random_seed", 0));
    }

    bool JsonFactory::loadPopulationConfig(
        PopulationConfigPtr cfg, const json::json &input)
    {
        if (input.find("population_config") == input.end())
        {
            LOG << LOG_LEVEL_ERROR << "Missing Population Conifg Section";
            return false;
        }
        json::json j = input.at("population_config");
        cfg->age_proportions = retrieve<std::array<double, 17>>(j, "age_proportions");
        cfg->age_contacts = retrieve<std::array<double, 17>>(j, "age_contacts");
        return true;
    }

    bool JsonFactory::loadInfectionConfig(
        InfectionConfigPtr cfg, const json::json &input)
    {
        if (input.find("infection_config") == input.end())
        {
            LOG << LOG_LEVEL_ERROR << "Missing Infection Config Section";
            return false;
        }
        json::json j = input.at("infection_config");
        cfg->infectionRadius = retrieve<double>(j, "infection_radius");
        cfg->basicReproductionNum = retrieve<double>(j, "basic_reproduction_num");
        cfg->probSymptomatic = retrieve<double>(j, "prob_symptomatic");
        cfg->symptInfectiousness = retrieve<double>(j, "sympt_infectiousness");
        cfg->asymptInfectiousness = retrieve<double>(j, "asympt_infectiousness");
        cfg->latentToSymptDelay = retrieve<double>(j, "latent_to_sympt_delay");

        cfg->falsePositiveRate = retrieve<double>(j, "false_positive_rate");
        cfg->householdTransmission = retrieve<double>(j, "household_transmission");
        cfg->placeTransmission = retrieve<double>(j, "place_transmission");
        cfg->meanPlaceGroupSize = retrieve<std::array<unsigned int, N_PLACE_GROUPS>>(j, "mean_place_group_size");
        cfg->spatial_distance_metric = retrieve<std::string>(j, "spatial_distance_metric");
        return true;
    }

    inline bool JsonFactory::loadTransitionTimeConfig(HostProgressionConfigPtr cfg, const json::json& input)
    {
        if (input.find("transition_time") == input.end())
        {
            LOG << LOG_LEVEL_ERROR << "Missing Host Progression Transition Time Config Section";
            return false;
        }
        json::json j = input.at("transition_time");
        cfg->latentPeriodICDF = retrieveICDF(j, "latent_period", "latent_period_icdf");
        cfg->asymptToRecovICDF = retrieveICDF(j, "asympt_infect_period", "asympt_infect_icdf");
        cfg->mildToRecovICDF = retrieveICDF(j, "mean_mild_to_recov", "mild_to_recov_icdf");
        cfg->gpToRecovICDF = retrieveICDF(j, "mean_gp_to_recov", "gp_to_recov_icdf");
        cfg->gpToHospICDF = retrieveICDF(j, "mean_gp_to_hosp", "gp_to_hosp_icdf");
        cfg->gpToDeathICDF = retrieveICDF(j, "mean_gp_to_death", "gp_to_death_icdf");
        cfg->hospToRecovICDF = retrieveICDF(j, "mean_hosp_to_recov", "hosp_to_recov_icdf");
        cfg->hospToICUICDF = retrieveICDF(j, "mean_hosp_to_icu", "hosp_to_icu_icdf");
        cfg->hospToDeathICDF = retrieveICDF(j, "mean_hosp_to_death", "hosp_to_death_icdf");
        cfg->icuToICURecovICDF = retrieveICDF(j, "mean_icu_to_icurecov", "icu_to_icurecov_icdf");
        cfg->icuToDeathICDF = retrieveICDF(j, "mean_icu_to_death", "icu_to_death_icdf");
        cfg->icuRecovToRecovICDF = retrieveICDF(j, "mean_icurecov_to_recov", "icurecov_to_recov_icdf");
        return true;
    }

    inline bool JsonFactory::loadTransitionStateConfig(HostProgressionConfigPtr cfg, const json::json& input)
    {
        if (input.find("transition_state") == input.end())
        {
            LOG << LOG_LEVEL_ERROR << "Missing Host Progression Transition State Config Section";
            return false;
        }
        json::json j = input.at("transition_state");
        cfg->prob_gp_to_hosp = retrieve<std::array<double, N_AGE_GROUPS>>(j, "prob_gp_to_hosp");
        cfg->prob_gp_to_recov = retrieve<std::array<double, N_AGE_GROUPS>>(j, "prob_gp_to_recov");
        cfg->prob_exposed_to_asympt = retrieve<std::array<double, N_AGE_GROUPS>>(j, "prob_exposed_to_asympt");
        cfg->prob_exposed_to_gp = retrieve<std::array<double, N_AGE_GROUPS>>(j, "prob_exposed_to_gp");
        cfg->prob_exposed_to_mild = retrieve<std::array<double, N_AGE_GROUPS>>(j, "prob_exposed_to_mild");
        cfg->prob_hosp_to_death = retrieve<std::array<double, N_AGE_GROUPS>>(j, "prob_hosp_to_death");
        cfg->prob_hosp_to_recov = retrieve<std::array<double, N_AGE_GROUPS>>(j, "prob_hosp_to_recov");
        cfg->prob_hosp_to_icu = retrieve<std::array<double, N_AGE_GROUPS>>(j, "prob_hosp_to_icu");
        cfg->prob_icu_to_death = retrieve<std::array<double, N_AGE_GROUPS>>(j, "prob_icu_to_death");
        cfg->prob_icu_to_icurecov = retrieve<std::array<double, N_AGE_GROUPS>>(j, "prob_icu_to_icurecov");
        return true;
    }

    bool JsonFactory::loadHostProgressionConfig(
        HostProgressionConfigPtr cfg, const json::json &input)
    {
        if (input.find("infection_config") != input.end() &&
            input["infection_config"].find("host_progression_config") == input["infection_config"].end())
        {
            LOG << LOG_LEVEL_ERROR << "Missing Host Progression Config Section";
            return false;
        }
        json::json j = input["infection_config"].at("host_progression_config");
        if (!(
                loadTransitionTimeConfig(cfg, j) &&
                loadTransitionStateConfig(cfg, j)))
            return false;
        
        cfg->use_ages = retrieve<bool>(j, "use_ages");
        cfg->infectiousness_profile = retrieve<std::vector<double>>(j, "infectiousness_profile");
        return true;
    }

    template <typename T>
    const T JsonFactory::retrieve(const json::json &input, const std::string &paramName)
    {
        if (input.find(paramName) == input.end())
        {
            LOG << LOG_LEVEL_ERROR << "Unable to retrieve parameter \"" << paramName << "\"";
            std::throw_with_nested(std::runtime_error("Missing required parameter"));
        }
        return input.at(paramName).get<T>();
    }

    template <typename T>
    const T JsonFactory::retrieve(const json::json &input, const std::string &paramName, const T &def)
    {
        if (input.find(paramName) == input.end())
        {
            LOG << LOG_LEVEL_WARNING << "Unable to retrieve parameter \"" << paramName << "\", using default value.";
            return def;
        }
        return input.at(paramName).get<T>();
    }

    InverseCDF JsonFactory::retrieveICDF(
        const json::json &input,
        const std::string& meanParamName,
        const std::string &icdfParamName)
    {
        std::vector<double> values = input.at(icdfParamName).get<std::vector<double>>();
        if (values.size() != InverseCDF::RES + 1)
        {
            LOG << LOG_LEVEL_ERROR << "Invalid number of values in " << icdfParamName;
            std::throw_with_nested(std::runtime_error("Error loading ICDF"));
        }

        InverseCDF icdf = InverseCDF(
            retrieve<double>(input, meanParamName));
        for (size_t i = 0; i < InverseCDF::RES + 1; i++)
        {
            icdf[i] = values[i];
        }
        return icdf;
    }

}
#include "json_factory.hpp"
#include "../logfile.hpp"

#include <iostream>
#include <fstream>

namespace epiabm
{

    JsonFactory::JsonFactory() :
        ConfigurationFactoryInterface()
    {}

    SimulationConfigPtr JsonFactory::loadConfig(const json::json& input)
    {
        SimulationConfigPtr config = std::make_shared<SimulationConfig>();
        loadSimulationConfig(config, input);
        if (!(
                loadInfectionConfig(config->infectionConfig, input) &&
                loadHostProgressionConfig(config->infectionConfig->hostProgressionConfig, input)))
            throw std::runtime_error("Json Factory Error Loading Config Files");
        return config;
    }

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
        cfg->latentPeriod = retrieve<double>(j, "latent_period");
        cfg->asymptInfectPeriod = retrieve<double>(j, "asympt_infect_period");
        cfg->probSymptomatic = retrieve<double>(j, "prob_symptomatic");
        cfg->symptInfectiousness = retrieve<double>(j, "sympt_infectiousness");
        cfg->asymptInfectiousness = retrieve<double>(j, "asympt_infectiousness");
        cfg->latentToSymptDelay = retrieve<double>(j, "latent_to_sympt_delay");

        cfg->falsePositiveRate = retrieve<double>(j, "false_positive_rate");
        cfg->householdTransmission = retrieve<double>(j, "household_transmission");
        cfg->placeTransmission = retrieve<double>(j, "place_transmission");
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
        cfg->meanMildToRecov = retrieve<double>(j, "mean_mild_to_recov");
        cfg->meanGPToRecov = retrieve<double>(j, "mean_gp_to_recov");
        cfg->meanGPToHosp = retrieve<double>(j, "mean_gp_to_hosp");
        cfg->meanGPToDeath = retrieve<double>(j, "mean_gp_to_death");
        cfg->meanHospToRecov = retrieve<double>(j, "mean_hosp_to_recov");
        cfg->meanHospToIcu = retrieve<double>(j, "mean_hosp_to_icu");
        cfg->meanHospToDeath = retrieve<double>(j, "mean_hosp_to_death");
        cfg->meanICUToICURecov = retrieve<double>(j, "mean_icu_to_icurecov");
        cfg->meanICUToDeath = retrieve<double>(j, "mean_icu_to_death");
        cfg->meanICURecovToRecov = retrieve<double>(j, "mean_icurecov_to_recov");

        cfg->latentPeriodICDF = retrieveICDF(j, "latent_period_icdf");
        cfg->asymptInfectICDF = retrieveICDF(j, "asympt_infect_icdf");
        cfg->mildToRecovICDF = retrieveICDF(j, "mild_to_recov_icdf");
        cfg->gpToRecovICDF = retrieveICDF(j, "gp_to_recov_icdf");
        cfg->gpToHospICDF = retrieveICDF(j, "gp_to_hosp_icdf");
        cfg->gpToDeathICDF = retrieveICDF(j, "gp_to_death_icdf");
        cfg->hospToRecovICDF = retrieveICDF(j, "hosp_to_recov_icdf");
        cfg->hospToICUICDF = retrieveICDF(j, "hosp_to_icu_icdf");
        cfg->hospToDeathICDF = retrieveICDF(j, "hosp_to_death_icdf");
        cfg->icuToICURecovICDF = retrieveICDF(j, "icu_to_icurecov_icdf");
        cfg->icuToDeathICDF = retrieveICDF(j, "icu_to_death_icdf");
        cfg->icuRecovToRecov = retrieveICDF(j, "icurecov_to_recov_icdf");
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

    InverseCDF JsonFactory::retrieveICDF(const json::json &input, const std::string &paramName)
    {
        std::vector<double> values = input.at(paramName).get<std::vector<double>>();
        if (values.size() != InverseCDF::RES + 1)
        {
            LOG << LOG_LEVEL_ERROR << "Invalid number of values in " << paramName;
            std::throw_with_nested(std::runtime_error("Error loading ICDF"));
        }

        InverseCDF icdf = InverseCDF();
        for (size_t i = 0; i < InverseCDF::RES + 1; i++)
        {
            icdf[i] = values[i];
        }
        return icdf;
    }

}
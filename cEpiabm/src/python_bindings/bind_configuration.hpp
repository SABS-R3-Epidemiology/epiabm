#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "configuration/host_progression_config.hpp"
#include "configuration/infection_config.hpp"
#include "configuration/simulation_config.hpp"
#include "configuration/config_factory_interface.hpp"
#include "configuration/json_factory.hpp"

namespace py = pybind11;

void bind_configuration(py::module &m)
{
    using namespace epiabm;

    py::class_<SimulationConfig, SimulationConfigPtr>(m, "SimulationConfig")
        .def_readwrite("timesteps_per_day", &SimulationConfig::timestepsPerDay, "Number of iterations per day")
        .def_readonly("infection_config", &SimulationConfig::infectionConfig, "Infection config section");

    py::class_<InfectionConfig, InfectionConfigPtr>(m, "InfectionConfig")
        .def_readwrite("basic_reproduction_number", &InfectionConfig::basicReproductionNum, "")
        .def_readwrite("infection_radius", &InfectionConfig::infectionRadius, "")
        .def_readwrite("prob_symptomatic", &InfectionConfig::probSymptomatic, "")
        .def_readwrite("sympt_infectiousness", &InfectionConfig::symptInfectiousness, "")
        .def_readwrite("asympt_infectiousness", &InfectionConfig::asymptInfectiousness, "")
        .def_readwrite("latent_to_sympt_delay", &InfectionConfig::latentToSymptDelay, "")
        .def_readwrite("false_positive_rate", &InfectionConfig::falsePositiveRate, "")
        .def_readwrite("household_transmission", &InfectionConfig::householdTransmission, "")
        .def_readwrite("place_transmission", &InfectionConfig::placeTransmission, "")
        .def_readonly("host_progression_config", &InfectionConfig::hostProgressionConfig, "Host Progression config section");

    py::class_<HostProgressionConfig, HostProgressionConfigPtr>(m, "HostProgressionConfig")
        .def_readonly("latent_period_icdf", &HostProgressionConfig::latentPeriodICDF, "iCDF for latent period duration")
        .def_readonly("asympt_to_recov_icdf", &HostProgressionConfig::asymptToRecovICDF, "iCDF for asympt to recov transition time")
        .def_readonly("mild_to_recov_icdf", &HostProgressionConfig::mildToRecovICDF, "iCDF for mild to recov transition time")
        .def_readonly("gp_to_recov_icdf", &HostProgressionConfig::gpToRecovICDF, "iCDF for gp to recov transition time")
        .def_readonly("gp_to_hosp_icdf", &HostProgressionConfig::gpToHospICDF, "iCDF for gp to hosp transition time")
        .def_readonly("gp_to_death_icdf", &HostProgressionConfig::gpToDeathICDF, "iCDF for gp to death transition time")
        .def_readonly("hosp_to_recov_icdf", &HostProgressionConfig::hospToRecovICDF, "iCDF for hosp to recov transition time")
        .def_readonly("hosp_to_icu_icudf", &HostProgressionConfig::hospToICUICDF, "iCDF for hosp to ICU transition time")
        .def_readonly("hosp_to_death_icdf", &HostProgressionConfig::hospToDeathICDF, "iCDF for hosp to death transition time")
        .def_readonly("icu_to_icurecov_icdf", &HostProgressionConfig::icuToICURecovICDF, "iCDF for icu to icu recov transition time")
        .def_readonly("icu_to_death_icdf", &HostProgressionConfig::icuToDeathICDF, "iCDF for icu to death transition time")
        .def_readonly("icurecov_to_recov_icdf", &HostProgressionConfig::icuRecovToRecovICDF, "iCDF for icu recov to recov transition time");


    py::class_<ConfigurationFactoryInterface, ConfigurationFactoryPtr>(m, "ConfigurationFactory")
        .def(py::init<>())
        .def("load_config", &ConfigurationFactoryInterface::loadConfig, "Create a SimulationConfig from config file",
            py::return_value_policy::take_ownership);
    
    py::class_<JsonFactory, JsonFactoryPtr>(m, "JsonFactory",
        py::base<ConfigurationFactoryInterface>())
        .def(py::init<>());

}

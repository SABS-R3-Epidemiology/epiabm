#ifndef EPIABM_CONFIGURATION_INFECTION_PROGRESSION_CONFIGURATION_HPP
#define EPIABM_CONFIGURATION_INFECTION_PROGRESSION_CONFIGURATION_HPP

#include "../utilities/inverse_cdf.hpp"
#include "../dataclasses/population.hpp"

#include <memory>
#include <array>

namespace epiabm
{

    class HostProgressionConfig
    {
    private:
    public:
        InverseCDF latentPeriodICDF;
        InverseCDF asymptToRecovICDF;
        InverseCDF mildToRecovICDF;
        InverseCDF gpToRecovICDF;
        InverseCDF gpToHospICDF;
        InverseCDF gpToDeathICDF;
        InverseCDF hospToRecovICDF;
        InverseCDF hospToICUICDF;
        InverseCDF hospToDeathICDF;
        InverseCDF icuToICURecovICDF;
        InverseCDF icuToDeathICDF;
        InverseCDF icuRecovToRecovICDF;

        bool use_ages;
        std::array<double, N_AGE_GROUPS> prob_gp_to_hosp;
        std::array<double, N_AGE_GROUPS> prob_gp_to_recov;
        std::array<double, N_AGE_GROUPS> prob_exposed_to_asympt;
        std::array<double, N_AGE_GROUPS> prob_exposed_to_gp;
        std::array<double, N_AGE_GROUPS> prob_exposed_to_mild;
        std::array<double, N_AGE_GROUPS> prob_hosp_to_death;
        std::array<double, N_AGE_GROUPS> prob_hosp_to_recov;
        std::array<double, N_AGE_GROUPS> prob_hosp_to_icu;
        std::array<double, N_AGE_GROUPS> prob_icu_to_death;
        std::array<double, N_AGE_GROUPS> prob_icu_to_icurecov;

        std::vector<double> infectiousness_profile;

    private:
    }; // class InfectionProgressionConfig

    typedef std::shared_ptr<HostProgressionConfig> HostProgressionConfigPtr;

} // namespace epiabm

#endif // EPIABM_CONFIGURATION_INFECTION_PROGRESSION_CONFIGURATION_HPP
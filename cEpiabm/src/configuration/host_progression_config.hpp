#ifndef EPIABM_CONFIGURATION_INFECTION_PROGRESSION_CONFIGURATION_HPP
#define EPIABM_CONFIGURATION_INFECTION_PROGRESSION_CONFIGURATION_HPP

#include "../utilities/inverse_cdf.hpp"

#include <memory>

namespace epiabm
{

    class HostProgressionConfig
    {
    private:
    public:
        double meanMildToRecov;
        double meanGPToRecov;
        double meanGPToHosp;
        double meanGPToDeath;
        double meanHospToRecov;
        double meanHospToIcu;
        double meanHospToDeath;
        double meanICUToICURecov;
        double meanICUToDeath;
        double meanICURecovToRecov;

        InverseCDF latentPeriodICDF;
        InverseCDF asymptInfectICDF;
        InverseCDF mildToRecovICDF;
        InverseCDF gpToRecovICDF;
        InverseCDF gpToHospICDF;
        InverseCDF gpToDeathICDF;
        InverseCDF hospToRecovICDF;
        InverseCDF hospToICUICDF;
        InverseCDF hospToDeathICDF;
        InverseCDF icuToICURecovICDF;
        InverseCDF icuToDeathICDF;
        InverseCDF icuRecovToRecov;

    private:
    }; // class InfectionProgressionConfig

    typedef std::shared_ptr<HostProgressionConfig> HostProgressionConfigPtr;

} // namespace epiabm

#endif // EPIABM_CONFIGURATION_INFECTION_PROGRESSION_CONFIGURATION_HPP
#ifndef EPIABM_DATACLASSES_INFECTION_STATUS_HPP
#define EPIABM_DATACLASSES_INFECTION_STATUS_HPP

#include <stdexcept>

namespace epiabm
{

    enum class InfectionStatus
    {
        Susceptible,
        Exposed,
        InfectASympt,
        InfectMild,
        InfectGP,
        InfectHosp,
        InfectICU,
        InfectICURecov,
        Recovered,
        Dead
    };

    constexpr const char* status_string(InfectionStatus status)
    {
        switch (status)
        {
            case InfectionStatus::Susceptible: return "Susceptible";
            case InfectionStatus::Exposed: return "Exposed";
            case InfectionStatus::InfectASympt: return "InfectASympt";
            case InfectionStatus::InfectMild: return "InfectMild";
            case InfectionStatus::InfectGP: return "InfectGP";
            case InfectionStatus::InfectHosp: return "InfectHosp";
            case InfectionStatus::InfectICU: return "InfectICU";
            case InfectionStatus::InfectICURecov: return "InfectICURecov";
            case InfectionStatus::Recovered: return "Recovered";
            case InfectionStatus::Dead: return "Dead";
            default: return "Unknown";
        }
    }
}

#endif // EPIABM_DATACLASSES_INFECTION_STATUS_HPP

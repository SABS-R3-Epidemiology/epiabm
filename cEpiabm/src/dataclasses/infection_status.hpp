#ifndef EPIABM_DATASTRUCTURES_TYPES_HPP
#define EPIABM_DATASTRUCTURES_TYPES_HPP

#include <memory>

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

} // namespace epiabm


#endif // EPIABM_DATASTRUCTURES_TYPES_HPP
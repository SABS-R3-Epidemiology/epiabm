#include "covidsim.hpp"


namespace epiabm
{
    double Covidsim::CalcHouseInf(
        Person* /*infector*/,
        unsigned short int )
    {
        return 1.0;
    }

    double Covidsim::CalcHouseSusc(
        Person* infector,
        Person* infectee,
        unsigned short int timestep)
    {
        return CalcPersonSusc(infector, infectee, timestep);
    }

    double Covidsim::CalcPersonSusc(
        Person* /*infector*/,
        Person* /*infectee*/,
        unsigned short int )
    {
        return 1.0;
    }


} // namespace epiabm
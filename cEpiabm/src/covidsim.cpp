#include "covidsim.hpp"


namespace epiabm
{
    double Covidsim::CalcHouseInf(
        Person* /*infector*/,
        unsigned short int )
    {
        return 1.0;
    }

    double Covidsim::CalcCellInf(
        Cell* cell,
        unsigned short int )
    {
        const int R_value = 2;
        return R_value * cell->numInfectious();
    }

    double Covidsim::CalcSpaceInf(
        Cell* /*cell*/,
        Person* /*infector*/,
        unsigned short int )
    {
        return 0.5;
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
    
    double Covidsim::CalcSpaceSusc(
        Cell* /*cell*/,
        Person* /*infectee*/,
        unsigned short int )
    {
        return 0.2;
    }


} // namespace epiabm
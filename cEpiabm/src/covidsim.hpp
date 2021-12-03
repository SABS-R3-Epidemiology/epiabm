#ifndef _EPIABM_COVIDSIM_HPP
#define _EPIABM_COVIDSIM_HPP

#include "dataclasses/person.hpp"

namespace epiabm
{

    class Covidsim
    {
        public:
        // Calculate Infectiveness Helpers
        static double CalcHouseInf(
            Person* infector,
            unsigned short int timestep);
        
        // Calculate Susceptibilities Helpers
        static double CalcHouseSusc(
            Person* infector,
            Person* infectee,
            unsigned short int timestep);
        static double CalcPersonSusc(
            Person* infector,
            Person* infectee,
            unsigned short int timestep);
    };

} // namespace epiabm

#endif // _EPIABM_COVIDSIM_HPP
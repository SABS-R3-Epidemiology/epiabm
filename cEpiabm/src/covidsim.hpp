#ifndef EPIABM_COVIDSIM_HPP
#define EPIABM_COVIDSIM_HPP

#include "dataclasses/person.hpp"
#include "dataclasses/cell.hpp"

namespace epiabm
{

    class Covidsim
    {
        public:
        // Calculate Infectiveness Helpers
        static double CalcHouseInf(
            Person* infector,
            unsigned short int timestep);
        static double CalcCellInf(
            Cell* cell,
            unsigned short int timestep);
        static double CalcSpaceInf(
            Cell* inf_cell,
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
        static double CalcSpaceSusc(
            Cell* cell,
            Person* infectee,
            unsigned short int timestep);
    };

} // namespace epiabm

#endif // EPIABM_COVIDSIM_HPP
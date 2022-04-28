#ifndef EPIABM_SRC_HOUSEHOLD_LINKER_HPP
#define EPIABM_SRC_HOUSEHOLD_LINKER_HPP


#include "dataclasses/population.hpp"


namespace epiabm
{


    class HouseholdLinker
    {
    private:
    public:

        /**
         * @brief Link households
         * Create n_households per microcell.
         * Person has percInHousehold to be in a household.
         * People who should be in a household are randomly assigned to a household in their microcell.
         * @param population 
         * @param n_households 
         * @param percInHousehold 
         */
        void linkHouseholds(
            PopulationPtr population,
            size_t n_households,
            int percInHousehold,
            size_t seed);

    private:
    }; // class HouseholdLinker


} // namespace epiabm

#endif // EPIABM_SRC_HOUSEHOLD_LINKER_HPP

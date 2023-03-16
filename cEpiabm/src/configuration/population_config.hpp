#ifndef EPIABM_CONFIGURATION_POPULATION_CONFIGURATION_HPP
#define EPIABM_CONFIGURATION_POPULATION_CONFIGURATION_HPP

#include "../dataclasses/population.hpp"

#include <memory>
#include <array>

namespace epiabm
{

    class PopulationConfig
    {
    private:
    public:
        std::array<double, N_AGE_GROUPS> age_proportions;
        std::array<double, N_AGE_GROUPS> age_contacts;

    private:
    }; // class PopulationConfigPtr

    typedef std::shared_ptr<PopulationConfig> PopulationConfigPtr;

} // namespace epiabm

#endif // EPIABM_CONFIGURATION_POPULATION_CONFIGURATION_HPP
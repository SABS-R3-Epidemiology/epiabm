#ifndef EPIABM_CONFIGURATION_INFECTION_CONFIGURATION_HPP
#define EPIABM_CONFIGURATION_INFECTION_CONFIGURATION_HPP

#include "host_progression_config.hpp"
#include "../dataclasses/place.hpp"

#include <memory>

namespace epiabm
{

    /**
     * @brief Configuration subclass for infection configuration options
     * 
     */
    class InfectionConfig
    {
        private:
        public:
            HostProgressionConfigPtr hostProgressionConfig;

            double basicReproductionNum;
            double infectionRadius;
            double probSymptomatic;
            double symptInfectiousness;
            double asymptInfectiousness;
            double latentToSymptDelay;

            double falsePositiveRate;

            double householdTransmission;
            double placeTransmission;

            std::array<unsigned int, N_PLACE_GROUPS> meanPlaceGroupSize;

            std::string spatial_distance_metric;

            /**
             * @brief Construct a new Infection Config object
             * 
             */
            InfectionConfig()
            {
                hostProgressionConfig = std::make_shared<HostProgressionConfig>();
            }
        private:
    };

    typedef std::shared_ptr<InfectionConfig> InfectionConfigPtr;

} // namespace epiabm


#endif // EPIABM_CONFIGURATION_INFECTION_CONFIGURATION_HPP
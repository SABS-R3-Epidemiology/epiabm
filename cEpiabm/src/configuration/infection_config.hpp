#ifndef EPIABM_CONFIGURATION_INFECTION_CONFIGURATION_HPP
#define EPIABM_CONFIGURATION_INFECTION_CONFIGURATION_HPP

#include "host_progression_config.hpp"

#include <memory>

namespace epiabm
{

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

            std::string spatial_distance_metric;

            InfectionConfig()
            {
                hostProgressionConfig = std::make_shared<HostProgressionConfig>();
            }
        private:
    };

    typedef std::shared_ptr<InfectionConfig> InfectionConfigPtr;

} // namespace epiabm


#endif // EPIABM_CONFIGURATION_INFECTION_CONFIGURATION_HPP
#ifndef EPIABM_REPORTERS_POPULATION_COMPARTMENT_REPORTER_HPP
#define EPIABM_REPORTERS_POPULATION_COMPARTMENT_REPORTER_HPP

#include "timestep_reporter_interface.hpp"


namespace epiabm
{


    class PopulationCompartmentReporter : public TimestepReporterInterface
    {
        private:
            std::set<InfectionStatus> m_compartments;
            ofstreamPtr m_os;

        public:
            PopulationCompartmentReporter(const std::string folder);
            ~PopulationCompartmentReporter() = default;

            void setup(const PopulationPtr population) override;

            void report(const PopulationPtr population, const unsigned short timestep) override;

            std::set<InfectionStatus>& compartments();

        private:
    };


} // namespace epiabm



#endif // EPIABM_REPORTERS_POPULATION_COMPARTMENT_REPORTER_HPP
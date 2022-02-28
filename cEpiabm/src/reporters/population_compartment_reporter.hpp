#ifndef EPIABM_REPORTERS_POPULATION_COMPARTMENT_REPORTER_HPP
#define EPIABM_REPORTERS_POPULATION_COMPARTMENT_REPORTER_HPP

#include "timestep_reporter_interface.hpp"


namespace epiabm
{

    /**
     * @brief Report total compartment counts each iteration for the entire population
     * Outputs a single file which contains the compartment counts over time
     */
    class PopulationCompartmentReporter : public TimestepReporterInterface
    {
        private:
            std::set<InfectionStatus> m_compartments;
            ofstreamPtr m_os;

        public:
            /**
             * @brief Construct a new Population Compartment Reporter object
             * If the file already exists, it will be overwritten
             * @param file File to write to
             */
            PopulationCompartmentReporter(const std::string file);
            ~PopulationCompartmentReporter() = default;

            /**
             * @brief Setup method which is called immediately before iterations begin
             * 
             * @param pop Initialized population before the iterations start
             */
            void setup(const PopulationPtr population) override;

            /**
             * @brief Report the population state at a timestep
             * 
             * @param pop Population to report
             * @param timestep Timestep of report
             */
            void report(const PopulationPtr population, const unsigned short timestep) override;

            /**
             * @brief Getter for set which contains the compartment types to return
             * This set can be configured to specify which compartments to output
             * @return std::set<InfectionStatus>& 
             */
            std::set<InfectionStatus>& compartments();

        private:
    };


} // namespace epiabm



#endif // EPIABM_REPORTERS_POPULATION_COMPARTMENT_REPORTER_HPP
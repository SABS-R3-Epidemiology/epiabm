#ifndef EPIABM_REPORTERS_PERCELL_COMPARTMENT_REPORTER
#define EPIABM_REPORTERS_PERCELL_COMPARTMENT_REPORTER

#include "timestep_reporter_interface.hpp"

#include <map>

namespace epiabm
{

    /**
     * @brief Report Compartment Counts each Iteration for Each Cell
     * Outputs to a folder with one file per cell with compartment counts over time
     */
    class PerCellCompartmentReporter : public TimestepReporterInterface
    {
        private:
            std::set<InfectionStatus> m_compartments;
            std::map<size_t, ofstreamPtr> m_cellFileMap;

        public:
            /**
             * @brief Construct a new Per Cell Compartment Reporter object
             * 
             * @param folder Folder to output to
             */
            PerCellCompartmentReporter(const std::string folder);
            ~PerCellCompartmentReporter() = default;

            /**
             * @brief Setup method which is called immediately before iterations begin
             * 
             * @param pop Initialized population before the iterations start
             */
            void setup(const PopulationPtr pop) override;

            /**
             * @brief Report the population state at a timestep
             * 
             * @param pop Population to report
             * @param timestep Timestep of report
             */
            void report(const PopulationPtr pop, const unsigned short timestep) override;

            /**
             * @brief Clean up method
             * Called after the simulation has completed to finalise the output files
             */
            void teardown() override;

            /**
             * @brief Getter for set which contains the compartment types to return
             * This set can be configured to specify which compartments to output
             * @return std::set<InfectionStatus>& 
             */
            std::set<InfectionStatus>& compartments();

        private:
    };


} // namespace epiabm


#endif // EPIABM_REPORTERS_PERCELL_COMPARTMENT_REPORTER

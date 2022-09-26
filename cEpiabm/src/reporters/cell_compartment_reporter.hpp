#ifndef EPIABM_REPORTERS_CELL_COMPARTMENT_REPORTER
#define EPIABM_REPORTERS_CELL_COMPARTMENT_REPORTER

#include "timestep_reporter_interface.hpp"


namespace epiabm
{

    /**
     * @brief Report Comportment Counts each iteration for each cell
     * Outputs to a folder with one csv each timestep with the compartment counts for each cell
     */
    class CellCompartmentReporter : public TimestepReporterInterface
    {
        private:
            std::set<InfectionStatus> m_compartments;

        public:
            /**
             * @brief Construct a new Cell Compartment Reporter object
             * 
             * @param folder Output Folder
             */
            CellCompartmentReporter(const std::string folder);
            ~CellCompartmentReporter() = default;

            /**
             * @brief Report the population state at a timestep
             * 
             * @param pop Population to report
             * @param timestep Timestep of report
             */
            void report(const PopulationPtr pop, const unsigned short timestep) override;

            /**
             * @brief Getter for set which contains the compartment types to return
             * This set can be configured to specify which compartments to output
             * @return std::set<InfectionStatus>& 
             */
            std::set<InfectionStatus>& compartments();

        private:
    };


    typedef std::shared_ptr<CellCompartmentReporter> CellCompartmentReporterPtr;

} // namespace epiabm


#endif // EPIABM_REPORTERS_CELL_COMPARTMENT_REPORTER

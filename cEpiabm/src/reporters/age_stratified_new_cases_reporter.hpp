#ifndef EPIABM_REPORTERS_AGE_STRATIFIED_NEW_CASES_REPORTER_HPP
#define EPIABM_REPORTERS_AGE_STRATIFIED_NEW_CASES_REPORTER_HPP

#include "timestep_reporter_interface.hpp"

#include <map>

namespace epiabm
{

    /**
     * @brief Report Compartment Counts each Iteration for Each Cell
     * Outputs to a folder with one file per cell with compartment counts over time
     */
    class AgeStratifiedNewCasesReporter : public TimestepReporterInterface
    {
    private:
        ofstreamPtr m_os;

    public:
        AgeStratifiedNewCasesReporter(const std::string file);
        ~AgeStratifiedNewCasesReporter();

        void setup(const PopulationPtr pop) override;

        void report(const PopulationPtr pop, const unsigned short timestep) override;

        void teardown() override;

    private:
    };

    typedef std::shared_ptr<AgeStratifiedNewCasesReporter> AgeStratifiedNewCasesReporterPtr;

} // namespace epiabm

#endif // EPIABM_REPORTERS_AGE_STRATIFIED_NEW_CASES_REPORTER_HPP

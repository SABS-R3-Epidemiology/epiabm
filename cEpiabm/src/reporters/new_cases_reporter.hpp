#ifndef EPIABM_REPORTERS_NEW_CASES_REPORTER_HPP
#define EPIABM_REPORTERS_NEW_CASES_REPORTER_HPP

#include "timestep_reporter_interface.hpp"

#include <map>

namespace epiabm
{

    /**
     * @brief Report Compartment Counts each Iteration for Each Cell
     * Outputs to a folder with one file per cell with compartment counts over time
     */
    class NewCasesReporter : public TimestepReporterInterface
    {
    private:
        ofstreamPtr m_os;

    public:
        NewCasesReporter(const std::string folder);
        ~NewCasesReporter();

        void setup(const PopulationPtr pop) override;

        void report(const PopulationPtr pop, const unsigned short timestep) override;

        void teardown() override;

    private:
    };

    typedef std::shared_ptr<NewCasesReporter> NewCasesReporterPtr;

} // namespace epiabm

#endif // EPIABM_REPORTERS_NEW_CASES_REPORTER_HPP

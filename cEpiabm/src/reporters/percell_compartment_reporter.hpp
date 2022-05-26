#ifndef EPIABM_REPORTERS_PERCELL_COMPARTMENT_REPORTER
#define EPIABM_REPORTERS_PERCELL_COMPARTMENT_REPORTER

#include "timestep_reporter_interface.hpp"

#include <map>

namespace epiabm
{


    class PerCellCompartmentReporter : public TimestepReporterInterface
    {
        private:
            std::set<InfectionStatus> m_compartments;
            std::map<size_t, ofstreamPtr> m_cellFileMap;

        public:
            PerCellCompartmentReporter(const std::string folder);
            ~PerCellCompartmentReporter() = default;

            void setup(const PopulationPtr pop) override;

            void report(const PopulationPtr pop, const unsigned short timestep) override;

            void teardown() override;

            std::set<InfectionStatus>& compartments();

        private:
    };

    typedef std::shared_ptr<PerCellCompartmentReporter> PerCellCompartmentReporterPtr;

} // namespace epiabm


#endif // EPIABM_REPORTERS_PERCELL_COMPARTMENT_REPORTER

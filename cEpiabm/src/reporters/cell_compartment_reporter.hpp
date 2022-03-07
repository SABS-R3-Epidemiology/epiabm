#ifndef EPIABM_REPORTERS_CELL_COMPARTMENT_REPORTER
#define EPIABM_REPORTERS_CELL_COMPARTMENT_REPORTER

#include "timestep_reporter_interface.hpp"


namespace epiabm
{


    class CellCompartmentReporter : public TimestepReporterInterface
    {
        private:
            std::set<InfectionStatus> m_compartments;

        public:
            CellCompartmentReporter(const std::string folder);
            ~CellCompartmentReporter() = default;

            void report(const PopulationPtr pop, const unsigned short timestep) override;

            std::set<InfectionStatus>& compartments();

        private:
    };

    typedef std::shared_ptr<CellCompartmentReporter> CellCompartmentReporterPtr;


} // namespace epiabm


#endif // EPIABM_REPORTERS_CELL_COMPARTMENT_REPORTER

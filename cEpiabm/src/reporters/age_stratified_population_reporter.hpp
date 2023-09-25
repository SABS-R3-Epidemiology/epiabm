#ifndef EPIABM_REPORTERS_AGE_STRATIFIED_POPULATION_REPORTER_HPP
#define EPIABM_REPORTERS_AGE_STRATIFIED_POPULATION_REPORTER_HPP

#include "timestep_reporter_interface.hpp"

namespace epiabm
{

    /**
     * @brief Report total compartment counts each iteration for the entire population
     * Outputs a single file which contains the compartment counts over time
     */
    class AgeStratifiedPopulationReporter : public TimestepReporterInterface
    {
    private:
        std::set<InfectionStatus> m_compartments;
        ofstreamPtr m_os;

    public:
        AgeStratifiedPopulationReporter(const std::string file);
        ~AgeStratifiedPopulationReporter();

        void setup(const PopulationPtr population) override;

        void report(const PopulationPtr population, const unsigned short timestep) override;

        std::set<InfectionStatus> &compartments();

    private:
    };

    typedef std::shared_ptr<AgeStratifiedPopulationReporter> AgeStratifiedPopulationReporterPtr;

} // namespace epiabm

#endif // EPIABM_REPORTERS_AGE_STRATIFIED_POPULATION_REPORTER_HPP
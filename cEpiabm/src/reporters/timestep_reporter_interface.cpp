
#include "timestep_reporter_interface.hpp"


namespace epiabm
{

    /**
     * @brief Constructor
     *
     * @param folder Folder to output to
     * @param clearfolder whether folder should be emptied at the start of the simulation
     */
    TimestepReporterInterface::TimestepReporterInterface(
        const std::string folder,
        bool clearfolder) :
        m_folder(std::filesystem::path(folder), clearfolder)
    {}

    /**
     * @brief Constructor
     *
     * @param folder Folder to output to
     * @param clearfolder whether folder should be emptied at the start of the simulation
     */
    TimestepReporterInterface::TimestepReporterInterface(
        const std::filesystem::path folder,
        bool clearfolder) :
        m_folder(folder, clearfolder)
    {}

    /**
     * @brief Destroy the Timestep Reporter Interface:: Timestep Reporter Interface object
     * 
     */
    TimestepReporterInterface::~TimestepReporterInterface(){}

    /**
     * @brief Setup method run immediately before iterations begin
     * Used for initializing required files
     * @param population Initialized population
     */
    void TimestepReporterInterface::setup(const PopulationPtr /*population*/) {}

    /**
     * @brief Report the population state at a timestep
     *
     * @param pop Population to report
     * @param timestep Timestep of report
     */
    void TimestepReporterInterface::report(const PopulationPtr /*population*/, unsigned short /*timestep*/) {}

    /**
     * @brief Clean up method
     * Called after the simulation has completed to finalise the output files
     */
    void TimestepReporterInterface::teardown() {}

} // namespace epiabm

#ifndef EPIABM_REPORTERS_TIMESTEP_REPORTER_INTERFACE
#define EPIABM_REPORTERS_TIMESTEP_REPORTER_INTERFACE


#include "../dataclasses/population.hpp"
#include "../output_folder_handler.hpp"

#include <ostream>
#include <memory>


namespace epiabm
{
    /**
     * @brief Interface for classes reporting on a population each iteration
     * 
     */
    class TimestepReporterInterface
    {
        protected:
            OutputFolderHandler m_folder;

        public:
            /**
             * @brief Constructor
             * 
             * @param folder Folder to output to
             * @param clearfolder whether folder should be emptied at the start of the simulation
             */
            TimestepReporterInterface(const std::string folder, bool clearfolder=false);
            /**
             * @brief Constructor
             * 
             * @param folder Folder to output to
             * @param clearfolder whether folder should be emptied at the start of the simulation
             */
            TimestepReporterInterface(const std::filesystem::path folder, bool clearfolder=false);
            virtual ~TimestepReporterInterface() {};

            /**
             * @brief Setup method run immediately before iterations begin
             * Used for initializing required files
             * @param population Initialized population
             */
            virtual void setup(const PopulationPtr population);

            /**
             * @brief Report the population state at a timestep
             * 
             * @param pop Population to report
             * @param timestep Timestep of report
             */
            virtual void report(const PopulationPtr population, const unsigned short timestep);

            /**
             * @brief Clean up method
             * Called after the simulation has completed to finalise the output files
             */
            virtual void teardown();

        private:
    }; // class TimestepReporterInterface

    typedef std::shared_ptr<TimestepReporterInterface> TimestepReporterInterfacePtr;

} // namespace epiabm


#endif // EPIABM_REPORTERS_TIMESTEP_REPORTER_INTERFACE

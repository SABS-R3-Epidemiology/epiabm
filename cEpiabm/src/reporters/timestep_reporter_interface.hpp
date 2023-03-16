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
        TimestepReporterInterface(const std::string folder, bool clearfolder = false);
        TimestepReporterInterface(const std::filesystem::path folder, bool clearfolder = false);
        virtual ~TimestepReporterInterface();

        virtual void setup(const PopulationPtr population);

        virtual void report(const PopulationPtr population, const unsigned short timestep);

        virtual void teardown();

    private:
    }; // class TimestepReporterInterface

    typedef std::shared_ptr<TimestepReporterInterface> TimestepReporterInterfacePtr;

} // namespace epiabm

#endif // EPIABM_REPORTERS_TIMESTEP_REPORTER_INTERFACE

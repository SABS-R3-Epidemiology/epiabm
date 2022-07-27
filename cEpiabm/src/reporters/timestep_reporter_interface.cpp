
#include "timestep_reporter_interface.hpp"


namespace epiabm
{

    TimestepReporterInterface::TimestepReporterInterface(
        const std::string folder,
        bool clearfolder) :
        m_folder(std::filesystem::path(folder), clearfolder)
    {}

    TimestepReporterInterface::TimestepReporterInterface(
        const std::filesystem::path folder,
        bool clearfolder) :
        m_folder(folder, clearfolder)
    {}

    void TimestepReporterInterface::setup(const PopulationPtr /*population*/) {}

    void TimestepReporterInterface::report(const PopulationPtr /*population*/, unsigned short /*timestep*/) {}

    void TimestepReporterInterface::teardown() {}

} // namespace epiabm

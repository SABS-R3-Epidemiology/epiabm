#include "output_folder_handler.hpp"


namespace epiabm
{

    OutputFolderHandler::OutputFolderHandler(
        const std::filesystem::path& directory_path,
        bool cleanOutputDirectory) :
        m_path(directory_path)
    {
        // Create directory
        std::filesystem::create_directories(directory_path);
        if (cleanOutputDirectory) // If should clear directory
        {
            std::filesystem::remove_all(directory_path); // Clear directory
            std::filesystem::create_directory(directory_path); // Recreate top directory
        }
    }

    ofstreamPtr OutputFolderHandler::OpenOutputFile(
        const std::string& filename,
        std::ios_base::openmode mode) const
    {
        return std::make_shared<std::ofstream>(m_path / filename, mode);
    }

} // namespace epiabm

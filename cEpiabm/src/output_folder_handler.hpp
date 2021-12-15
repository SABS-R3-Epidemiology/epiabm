#ifndef EPIABM_OUTPUT_FOLDER_HANDLER_HPP
#define EPIABM_OUTPUT_FOLDER_HANDLER_HPP


#include <memory>
#include <fstream>
#include <filesystem>


namespace epiabm
{
    typedef std::shared_ptr<std::ofstream> ofstreamPtr;

    /**
     * @brief Output Folder Handling Class
     * Class which handles opening a folder
     * Creates folder if it doesn't exist
     * Can clear the folder after opening
     * Public method which allows opening a file within this folder for writing
     */
    class OutputFolderHandler
    {
        private:
            const std::filesystem::path m_path;

        public:
            /**
             * @brief Construct a new Output File Handler object
             * 
             * @param directory_path Path to output directory
             * @param cleanOutputDirectory Flag whether to clear contents of output directory
             */
            OutputFolderHandler(
                const std::filesystem::path& directory_path,
                bool cleanOutputDirectory = true);

            /**
             * @brief Make outputfile and return ofstream for the file
             * Construct a new file inside of the OutputFolderHandler's directory.
             * @param rFileName New filename
             * @param mode std::ios_base::openmode Mode with which to open file
             * @return ofstreamPtr 
             */
            ofstreamPtr OpenOutputFile(
                const std::string& rFileName,
                std::ios_base::openmode mode = std::ios::out | std::ios::trunc) const;

    };
}


#endif // EPIABM_OUTPUT_FOLDER_HANDLER_HPP
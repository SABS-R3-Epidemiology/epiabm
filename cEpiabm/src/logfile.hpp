#ifndef EPIABM_LOGFILE_HPP
#define EPIABM_LOGFILE_HPP


#include "output_folder_handler.hpp"

#include <iostream>
#include <cstdint>
#include <filesystem>
#include <string>
#include <chrono>
#include <mutex>
#include <map>


namespace epiabm
{

    /**
     * @brief Class to handle logging
     * Singleton LogFile structure
     * Usage:
     *      // Configure
     *      std::filesystem::path logfilepath("log.log") // path to log file
     *      LogFile::Instance()->configure(0, logfilepath); // Configure logger
     *      // ALTERNATIVELY LOG.configure(0, logfilepath);
     * 
     *      // Write to Logs
     *      LOG << LOG_LEVEL_ERROR << "Encountered Error" << std::endl;
     *      LOG << LOG_LEVEL_NORMAL << "Started Simulation" << std::endl;
     *      
     *      // Cleanup
     *      LogFile::Close();
     */
    class LogFile
    {
    private:
        static LogFile* m_instance; // Singleton instance
        bool m_fileSet; // Bool representing whether file has been opened and m_os has been set
        ofstreamPtr m_os; // std::shared_ptr<std::ofstream> to log file

        unsigned int m_level; // Desired logging level
        bool m_active; // Whether logger is active (this is used for log level handling. Set to inactive if current statement is below current logging level)
        bool m_cout_enabled; // Boolean whether logger should log to cout aswell as file
        unsigned int m_precision; // Output precision for floating points

        static const unsigned int MAX_LOGGING_LEVEL = 5; // Maximum logging level for sanity check
        static const std::map<unsigned int, std::string> LEVEL_STRINGS; // Map of log level to text representation of log level

        std::mutex m_mutex; // Logging mutex for multithreading

    public:
        /**
         * @brief Singleton Instance
         * Return the Singleton LogFile Instance.
         * @return LogFile*
         */
        static LogFile* Instance();

        /**
         * @brief Current Logging Level
         * Return the current logging level
         * @return unsigned int
         */
        static unsigned int Level();

        /**
         * Close the currently open file, and delete the single LogFile instance.
         */
        void configure(unsigned int level, std::filesystem::path path);

        /**
         * Set the current logging level
         */
        void setLevel(unsigned int level);

        /**
         * Prepare the logger to recieve a log line by configuring the log level
         */
        const std::string prepare(unsigned int level);

        /**
         * Close the currently open file, and delete the single LogFile instance.
         */
        static void Close();

        /**
         * @return true if Set() has been called.
         */
        bool isFileSet() const;

        /**
         * Lock the logfile for multithreaded logging
         */
        void lock();

        /**
         * Unlock the logfile for multithreaded logging
         */
        void unlock();

        /**
         * Configure the logger to output to both std::cout and the output file
         */
        void enable_cout();

        /**
         * Configure the logger to output to output file only and not std::cout
         */
        void disable_cout();

    private:
        LogFile(); // private constructor (singleton);

        template <class T>
        friend LogFile& operator<<(LogFile& file, const T message);
    }; // class LogFile

    /**
     * @return reference to this object (as convention)
     * Overloaded << operator, to write to the log file, if one has been set, and
     * does nothing if not.
     *
     * @param message the message to write to the log file
     */
    template <class T>
    LogFile& operator<<(LogFile& file, const T message)
    {
        if (file.m_active)
        {
            auto& os = file.m_fileSet ? (*file.m_os) : std::cout;
            os << std::setprecision(static_cast<int>(file.m_precision))
                << message << std::flush;
        }
        return file;
    }

    // Macro getting the logger
    #define LOG *(epiabm::LogFile::Instance())

    // Macro for setting the log level
    #define LOG_LEVEL_DEBUG epiabm::LogFile::Instance()->prepare(0)
    #define LOG_LEVEL_INFO  epiabm::LogFile::Instance()->prepare(1)
    #define LOG_LEVEL_NORMAL epiabm::LogFile::Instance()->prepare(2)
    #define LOG_LEVEL_WARNING epiabm::LogFile::Instance()->prepare(3)
    #define LOG_LEVEL_ERROR epiabm::LogFile::Instance()->prepare(4)

} // namespace epiabm


#endif // EPIABM_LOGGER_HPP

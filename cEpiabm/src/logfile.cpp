
#include "logfile.hpp"


namespace epiabm
{
    LogFile* LogFile::m_instance = nullptr;

    LogFile::LogFile() :
        m_fileSet(false),
        m_level(0),
        m_active(true),
        m_cout_enabled(false),
        m_precision(3),
        m_mutex()
    {}

    LogFile* LogFile::Instance()
    {
        if (m_instance == nullptr)
            m_instance = new LogFile();
        return m_instance;
    }

    unsigned int LogFile::Level()
    {
        if (m_instance == nullptr) return 0;
        return m_instance->m_level;
    }

    void LogFile::configure(unsigned int level, std::filesystem::path path)
    {
        if (level > MAX_LOGGING_LEVEL) // Sanity check log level
        {
            // TODO: Add Custom Exception Handling Classes;
            throw std::runtime_error("Invalid Log Level");
        }
        m_level = level;

        OutputFolderHandler handler(path.parent_path(), false); // Open folder without deleting contents
        m_os = handler.OpenOutputFile(path.filename());
        m_fileSet = true;
    }
    
    const std::string LogFile::prepare(unsigned int level)
    {
        m_active = level >= m_level;
        if (!m_active) return "";

        // Get current time
        std::time_t time_now_t = std::chrono::system_clock::to_time_t(
            std::chrono::system_clock::now());
        std::tm tm = *std::localtime(&time_now_t);

        // Write header
        *m_os << std::endl << LogFile::LEVEL_STRINGS.at(level) << " ["
            << std::put_time(&tm, "%Y/%m/%d %H:%M:%S") << "]: ";
        return "";
    }

    void LogFile::Close()
    {
        if (m_instance != nullptr)
        {
            if (m_instance->m_fileSet) m_instance->m_os->close();
            delete m_instance;
            m_instance = nullptr;
        }
    }

    bool LogFile::isFileSet() const
    {
        return m_fileSet;
    }

    void LogFile::lock()
    {
        m_mutex.lock();
    }

    void LogFile::unlock()
    {
        m_mutex.unlock();
    }

    void LogFile::enable_cout()
    {
        m_cout_enabled = true;
    }

    void LogFile::disable_cout()
    {
        m_cout_enabled = false;
    }

    const std::map<unsigned int, std::string> LogFile::LEVEL_STRINGS = 
        {{0, "DEBUG"}, {1, "INFO"}, {2, "NORMAL"}, {3, "WARNING"}, {4, "ERROR"}};

} // namespace epiabm

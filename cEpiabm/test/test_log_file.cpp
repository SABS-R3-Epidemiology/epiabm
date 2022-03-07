
#include "logfile.hpp"

#include "catch/catch.hpp"

#include <filesystem>
#include <fstream>
#include <random>
#include <iostream>

using namespace epiabm;

TEST_CASE("logfile: test configure", "[LogFile]")
{
    std::filesystem::path logfile("output/test.log");
    std::filesystem::remove(logfile);
    LogFile::Instance()->configure(0, logfile);
    REQUIRE(std::filesystem::exists(logfile));
    LogFile::Close();

    REQUIRE_THROWS(LogFile::Instance()->configure(10, logfile));
}

TEST_CASE("logfile: test write", "[LogFile]")
{
    std::filesystem::path logfile("output/test.log");
    std::filesystem::remove(logfile);
    LogFile::Instance()->configure(0, logfile);
    REQUIRE(std::filesystem::exists(logfile));

    LOG << LOG_LEVEL_NORMAL << "Hello World! This is a Normal Log";
    LOG << LOG_LEVEL_WARNING << "DANGER!!!";
    LOG << LOG_LEVEL_INFO << "Extra Information";
    LOG << LOG_LEVEL_DEBUG << "Debug Log";
    LOG << LOG_LEVEL_ERROR << "Encountered an Error...";

    LogFile::Close();
}

TEST_CASE("logfile: test log level", "[LogFile]")
{
    std::filesystem::path logfile("output/test2.log");
    std::filesystem::remove(logfile);
    LogFile::Instance()->configure(3, logfile);
    REQUIRE(std::filesystem::exists(logfile));

    LOG << LOG_LEVEL_NORMAL << "Hello World! This is a Normal Log";
    LOG << LOG_LEVEL_WARNING << "DANGER!!!";
    LOG << LOG_LEVEL_INFO << "Extra Information";
    LOG << LOG_LEVEL_DEBUG << "Debug Log";
    LOG << LOG_LEVEL_ERROR << "Encountered an Error...";
    LogFile::Close();

    int num_lines = 0;
    std::ifstream f(logfile);
    std::string s;
    while (getline(f, s)) num_lines++;
    REQUIRE(num_lines == 3);
}

TEST_CASE("logfile: test isFileSet", "[LogFile]")
{
    std::filesystem::path logfile("output/test3.log");
    std::filesystem::remove(logfile);
    REQUIRE(LogFile::Instance()->isFileSet() == false);
    LogFile::Instance()->configure(2, logfile);
    REQUIRE(std::filesystem::exists(logfile));
    REQUIRE(LogFile::Instance()->isFileSet() == true);
    LogFile::Close();
    REQUIRE(LogFile::Instance()->isFileSet() == false);
    std::filesystem::remove(logfile);
    LogFile::Close();
    REQUIRE(LogFile::Instance()->isFileSet() == false);
}

TEST_CASE("logfile: test Level", "[LogFile]")
{
    std::filesystem::path logfile("output/test3.log");
    std::filesystem::remove(logfile);
    REQUIRE(LogFile::Instance()->Level() == 0);
    LogFile::Instance()->configure(2, logfile);
    REQUIRE(std::filesystem::exists(logfile));
    REQUIRE(LogFile::Instance()->Level() == 2);
    LogFile::Close();
    REQUIRE(LogFile::Instance()->Level() == 0);
    std::filesystem::remove(logfile);
    LogFile::Close();
    REQUIRE(LogFile::Instance()->Level() == 0);
}

TEST_CASE("logfile: test others", "[LogFile]")
{
    std::filesystem::path logfile("output/test3.log");
    std::filesystem::remove(logfile);
    LogFile::Instance()->lock();
    LogFile::Instance()->unlock();
    LogFile::Instance()->enable_cout();
    LogFile::Instance()->disable_cout();
    LogFile::Instance()->setLevel(2);
}

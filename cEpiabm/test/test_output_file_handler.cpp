
#include "output_folder_handler.hpp"

#include "catch/catch.hpp"

#include <filesystem>
#include <fstream>
#include <random>
#include <iostream>

using namespace epiabm;

TEST_CASE("output_folder_handler: test make output folder", "[OutputFolderHandler]")
{
    std::filesystem::path directory("output");
    OutputFolderHandler handler(directory);
    
    REQUIRE(std::filesystem::exists(directory));
}

TEST_CASE("output_folder_handler: test make output file", "[OutputFolderHandler]")
{
    std::filesystem::path directory("output");
    OutputFolderHandler handler(directory, true);
    std::string filename = std::to_string(std::rand()) + std::to_string(std::rand()) + ".txt";

    REQUIRE(std::filesystem::exists(directory));
    ofstreamPtr os = handler.OpenOutputFile(filename);
    REQUIRE(std::filesystem::exists(directory/filename));

    *os << "Hello World!" << std::endl;
    os->close();

    std::ifstream f(directory/filename);
    std::string s;
    getline(f, s);
    REQUIRE(s == "Hello World!");
}

TEST_CASE("output_folder_handler: test clear output folder", "[OutputFolderHandler]")
{
    std::filesystem::path directory("output");
    {
        OutputFolderHandler handler(directory, true);
        REQUIRE(std::filesystem::exists(directory));
        for (int i = 0; i < 10; i++)
        {
            std::string filename = std::to_string(i) + "_" + 
                std::to_string(std::rand()) + ".txt";
            ofstreamPtr os = handler.OpenOutputFile(filename);
            os->close();
            REQUIRE(std::filesystem::exists(directory/filename));
        }
    }

    auto requireFileCount = [&](int n)
    {
        int file_count = 0;
        for ([[maybe_unused]] const auto& f : std::filesystem::directory_iterator{directory})
            file_count++;
        REQUIRE(file_count == n);
    };

    requireFileCount(10);

    {
        OutputFolderHandler handler(directory, false);
        REQUIRE(std::filesystem::exists(directory));
        for (int i = 0; i < 10; i++)
        {
            std::string filename = std::to_string(i+100) + "_" +
                std::to_string(std::rand()) + ".txt";
            ofstreamPtr os = handler.OpenOutputFile(filename);
            os->close();
            REQUIRE(std::filesystem::exists(directory/filename));
        }
    }

    requireFileCount(20);

    {
        OutputFolderHandler handler(directory, true);
        REQUIRE(std::filesystem::exists(directory));
        for (int i = 0; i < 10; i++)
        {
            std::string filename = std::to_string(i) + "_" +
                std::to_string(std::rand()) + ".txt";
            ofstreamPtr os = handler.OpenOutputFile(filename);
            os->close();
            REQUIRE(std::filesystem::exists(directory/filename));
        }
    }

    requireFileCount(10);

    OutputFolderHandler handler(directory, true);
    REQUIRE(std::filesystem::exists(directory));
    requireFileCount(0);
}

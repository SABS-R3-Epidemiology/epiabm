

#include "utilities/random_manager.hpp"

#include "../catch/catch.hpp"

#include <random>
#include <thread>
#include <future>

using namespace epiabm;

TEST_CASE("utilities/random_manager: test constructor", "[RandomManager]")
{
    RandomManagerPtr subject = std::make_shared<RandomManager>(10);
}

TEST_CASE("utilities/random_manager: get generator", "[RandomManager]")
{
    RandomManagerPtr subject = std::make_shared<RandomManager>(100);
    REQUIRE_NOTHROW(subject->g());
}

TEST_CASE("utilitie/random_manager: multithreaded function test", "[RandomManager]")
{
    RandomManagerPtr subject = std::make_shared<RandomManager>(100);

    auto doStuff = [](RandomManagerPtr sub, size_t nReps)
    {
        for (size_t i = 0; i < nReps; i++) REQUIRE_NOTHROW(sub->g().generator()());
    };

    std::vector<std::thread> threads = std::vector<std::thread>();
    for (size_t i = 0; i < threads.size(); i++)
    {
        threads.emplace_back(doStuff, subject, i*1000);
    }

    for (size_t i = 0; i < threads.size(); i++)
    {
        threads[i].join();
    }
}

std::vector<unsigned long long> doStuff(RandomManagerPtr subject, size_t nReps)
{
    std::vector<unsigned long long> data = std::vector<unsigned long long>(nReps);
    for (size_t i = 0; i < nReps; i++) data[i] = static_cast<unsigned long long>(subject->g().generator()());
    return data;
}

TEST_CASE("utilities/random_manager: multithreaded repeatability test", "[RandomManager]")
{
    std::map<size_t, std::vector<unsigned long long>> original;
    const size_t seed = 100;
    const size_t nThreads = 10;
    const size_t nSamples = 1000;
    const size_t nReps = 10;

    {
        RandomManagerPtr subject = std::make_shared<RandomManager>(seed);
        for (size_t i = 0; i < nThreads; i++)
        {
            std::future<std::vector<unsigned long long>> ret = std::async(&doStuff, subject, nSamples);
            original[i] = ret.get();
            REQUIRE(original[i].size() == nSamples);
        }
    }

    for (size_t t = 0; t < nReps; t++)
    {
        RandomManagerPtr subject = std::make_shared<RandomManager>(seed);
        for (size_t i = 0; i < nThreads; i++)
        {
            std::future<std::vector<unsigned long long>> ret = std::async(&doStuff, subject, nSamples);
            std::vector<unsigned long long> compare = ret.get();

            REQUIRE(compare.size() == nSamples);
            REQUIRE(original[i].size() == nSamples);
            for (size_t j = 0; j < nSamples; j++)
            {
                REQUIRE(original[i][j] == compare[j]);
            }
        }
    }
}

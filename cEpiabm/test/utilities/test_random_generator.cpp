

#include "utilities/random_generator.hpp"

#include "../catch/catch.hpp"

#include <random>
#include <thread>
#include <future>

using namespace epiabm;

TEST_CASE("utilities/random_generator: test constructor", "[RandomGenerator]")
{
    RandomGeneratorPtr s1 = std::make_shared<RandomGenerator>(10, 0);
    RandomGeneratorPtr s2 = std::make_shared<RandomGenerator>(10, 1, std::this_thread::get_id());
    REQUIRE_NOTHROW(s1->generator()());
}

template <typename T>
std::vector<T> generateInts(RandomGeneratorPtr subject, size_t nSamples)
{
    std::vector<T> data;
    for (size_t i = 0; i < nSamples; i++)
    {
        data.push_back(subject->randi<T>(0, 1000));
    }
    return data;
}

template <typename T>
std::vector<T> generateFloats(RandomGeneratorPtr subject, size_t nSamples)
{
    std::vector<T> data;
    for (size_t i = 0; i < nSamples; i++)
    {
        data.push_back(subject->randf<T>());
    }
    return data;
}

TEST_CASE("utilities/random_generator: generate integers", "[RandomGenerator]")
{
    RandomGeneratorPtr subject = std::make_shared<RandomGenerator>(10, 0);
    
    REQUIRE_NOTHROW(subject->randi<int>(10));
    REQUIRE_NOTHROW(subject->randi<long>(10));
    REQUIRE_NOTHROW(subject->randi<unsigned int>(10));
    REQUIRE_NOTHROW(subject->randi<unsigned long>(10));

    REQUIRE_NOTHROW(subject->randi<int>(10, 100));
    REQUIRE_NOTHROW(subject->randi<long>(10, 100));
    REQUIRE_NOTHROW(subject->randi<unsigned int>(10, 100));
    REQUIRE_NOTHROW(subject->randi<unsigned long>(10, 100));
}

TEST_CASE("utilities/random_generator: generate floating points", "[RandomGenerator]")
{
    RandomGeneratorPtr subject = std::make_shared<RandomGenerator>(10, 0);
    
    REQUIRE_NOTHROW(subject->randf<float>());
    REQUIRE_NOTHROW(subject->randf<double>());
}

template <typename T>
void repeatabilityTestInts(size_t seed, size_t nReps, size_t nSamples)
{
    std::vector<T> original = generateInts<T>(std::make_shared<RandomGenerator>(seed, 0), nSamples);
    REQUIRE(original.size() == nSamples);
    for (size_t r = 0; r < nReps; r++)
    {
        std::vector<T> compare = generateInts<T>(std::make_shared<RandomGenerator>(seed, r), nSamples);
        REQUIRE(compare.size() == nSamples);
        REQUIRE(compare.size() == original.size());

        for (size_t i = 0; i < nSamples; i++)
        {
            REQUIRE(compare[i] == original[i]);
        }
    }
}

template <typename T>
void repeatabilityTestFloats(size_t seed, size_t nReps, size_t nSamples)
{
    std::vector<T> original = generateFloats<T>(std::make_shared<RandomGenerator>(seed, 0), nSamples);
    REQUIRE(original.size() == nSamples);
    for (size_t r = 0; r < nReps; r++)
    {
        std::vector<T> compare = generateFloats<T>(std::make_shared<RandomGenerator>(seed, r), nSamples);
        REQUIRE(compare.size() == nSamples);
        REQUIRE(compare.size() == original.size());

        for (size_t i = 0; i < nSamples; i++)
        {
            REQUIRE(compare[i] == original[i]);
        }
    }
}

TEST_CASE("utilities/random_generator: test repeatability", "[RandomGenerator]")
{
    for (size_t i = 0; i < 10; i++)
    {
        repeatabilityTestInts<int>(static_cast<size_t>(std::rand()), 5, 1000);
        repeatabilityTestInts<long>(static_cast<size_t>(std::rand()), 5, 1000);
        repeatabilityTestInts<unsigned int>(static_cast<size_t>(std::rand()), 5, 1000);
        repeatabilityTestInts<unsigned long>(static_cast<size_t>(std::rand()), 5, 1000);

        repeatabilityTestFloats<float>(static_cast<size_t>(std::rand()), 5, 1000);
        repeatabilityTestFloats<double>(static_cast<size_t>(std::rand()), 5, 1000);
    }

}

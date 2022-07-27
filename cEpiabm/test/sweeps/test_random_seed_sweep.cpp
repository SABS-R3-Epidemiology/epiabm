

#include "sweeps/random_seed_sweep.hpp"
#include "population_factory.hpp"
#include "configuration/json_factory.hpp"

#include "../catch/catch.hpp"
#include "helpers.hpp"

#include <random>

using namespace epiabm;

TEST_CASE("sweeps/random_seed_sweep: test initialize random_seed_sweep", "[RandomSeedSweep]")
{
    RandomSeedSweepPtr subject = std::make_shared<RandomSeedSweep>(
        std::make_shared<SimulationConfig>(), 1000);
}

TEST_CASE("sweeps/random_seed_sweep: test random_seed_sweep bind_population", "[RandomSeedSweep]")
{
    RandomSeedSweepPtr subject = std::make_shared<RandomSeedSweep>(
        std::make_shared<SimulationConfig>(), 1000);
    PopulationPtr population = PopulationFactory().makePopulation(5, 5, 1000);
    population->initialize();
    REQUIRE_NOTHROW(subject->bind_population(population));
}

TEST_CASE("sweeps/random_seed_sweep: test random_seed_sweep run sweep", "[RandomSeedSweep]")
{
    RandomSeedSweepPtr subject = std::make_shared<RandomSeedSweep>(
        JsonFactory().loadConfig(std::filesystem::path("../testdata/test_config.json")), 1000);
    PopulationPtr population = PopulationFactory().makePopulation(5, 5, 1000);
    random_seed(population, 10, InfectionStatus::InfectASympt, 5);
    random_seed(population, 10, InfectionStatus::Exposed, 2);
    population->initialize();
    REQUIRE_NOTHROW(subject->bind_population(population));
    for (int i = 0; i < 10; i++)
        REQUIRE_NOTHROW((*subject)(static_cast<unsigned short>(i)));
}

TEST_CASE("sweeps/random_seed_sweep: test destructor", "[RandomSeedSweep]")
{
    {
        SweepInterface* i = new RandomSeedSweep(
            std::make_shared<SimulationConfig>(), 1000);
        [[maybe_unused]] RandomSeedSweep* subject = dynamic_cast<RandomSeedSweep*>(i);
        delete i;
        i = nullptr;
        subject = nullptr;
    }
}

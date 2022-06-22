

#include "sweeps/basic_host_progression_sweep.hpp"
#include "population_factory.hpp"
#include "configuration/json_factory.hpp"

#include "../catch/catch.hpp"
#include "helpers.hpp"

#include <random>

using namespace epiabm;

TEST_CASE("sweeps/basic_host_progression_sweep: test initialize basic_host_progression_sweep", "[BasicHostProgressionSweep]")
{
    BasicHostProgressionSweepPtr subject = std::make_shared<BasicHostProgressionSweep>(
        std::make_shared<SimulationConfig>());
}

TEST_CASE("sweeps/basic_host_progression_sweep: test basic_host_progression_sweep bind_population", "[BasicHostProgressionSweep]")
{
    BasicHostProgressionSweepPtr subject = std::make_shared<BasicHostProgressionSweep>(
        std::make_shared<SimulationConfig>());
    PopulationPtr population = PopulationFactory().makePopulation(5, 5, 1000);
    population->initialize();
    REQUIRE_NOTHROW(subject->bind_population(population));
}

TEST_CASE("sweeps/basic_host_progression_sweep: test basic_host_progression_sweep run sweep", "[BasicHostProgressionSweep]")
{
    BasicHostProgressionSweepPtr subject = std::make_shared<BasicHostProgressionSweep>(
        JsonFactory().loadConfig(std::filesystem::path("../testdata/test_config.json")));
    PopulationPtr population = PopulationFactory().makePopulation(5, 5, 1000);
    random_seed(population, 10, InfectionStatus::InfectASympt, 5);
    random_seed(population, 10, InfectionStatus::Exposed, 2);
    population->initialize();
    REQUIRE_NOTHROW(subject->bind_population(population));
    for (int i = 0; i < 10; i++)
        REQUIRE_NOTHROW((*subject)(static_cast<unsigned short>(i)));
}

TEST_CASE("sweeps/basic_host_progression_sweep: test destructor", "[BasicHostProgressionSweep]")
{
    {
        SweepInterface* i = new BasicHostProgressionSweep(
            std::make_shared<SimulationConfig>());
        [[maybe_unused]] BasicHostProgressionSweep* subject = dynamic_cast<BasicHostProgressionSweep*>(i);
        delete i;
        i = nullptr;
        subject = nullptr;
    }
}

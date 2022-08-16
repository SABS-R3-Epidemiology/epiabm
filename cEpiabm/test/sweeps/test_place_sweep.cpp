

#include "sweeps/place_sweep.hpp"
#include "population_factory.hpp"
#include "configuration/simulation_config.hpp"
#include "configuration/json_factory.hpp"

#include "../catch/catch.hpp"
#include "helpers.hpp"

#include <random>

using namespace epiabm;

TEST_CASE("sweeps/place_sweep: test initialize place_sweep", "[PlaceSweep]")
{
    PlaceSweepPtr subject = std::make_shared<PlaceSweep>(
        std::make_shared<SimulationConfig>());
}

TEST_CASE("sweeps/place_sweep: test place_sweep bind_population", "[PlaceSweep]")
{
    PlaceSweepPtr subject = std::make_shared<PlaceSweep>(
        std::make_shared<SimulationConfig>());
    PopulationPtr population = PopulationFactory().makePopulation(5, 5, 1000);
    bind_places(population, 500, 10);
    population->initialize();
    REQUIRE_NOTHROW(subject->bind_population(population));
}

TEST_CASE("sweeps/place_sweep: test place_sweep run sweep", "[PlaceSweep]")
{
    PlaceSweepPtr subject = std::make_shared<PlaceSweep>(
        JsonFactory().loadConfig(std::filesystem::path("../testdata/test_config.json")));
    PopulationPtr population = PopulationFactory().makePopulation(5, 5, 1000);
    bind_places(population, 50, 10);
    random_seed(population, 10, InfectionStatus::InfectASympt, 5);
    population->initialize();
    REQUIRE_NOTHROW(subject->bind_population(population));
    for (int i = 0; i < 10; i++)
        REQUIRE_NOTHROW((*subject)(static_cast<unsigned short>(i)));
}

TEST_CASE("sweeps/place_sweep: test destructor", "[PlaceSweep]")
{
    {
        SweepInterface* i = new PlaceSweep(
            std::make_shared<SimulationConfig>());
        [[maybe_unused]] PlaceSweep* subject = dynamic_cast<PlaceSweep*>(i);
        delete i;
        i = nullptr;
        subject = nullptr;
    }
    {
        SweepInterface* i = new SweepInterface();
        i->operator()(0);
        i->cellCallback(0, nullptr);
        delete i;
        i = nullptr;
    }
}


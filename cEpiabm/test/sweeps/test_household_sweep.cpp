

#include "sweeps/household_sweep.hpp"
#include "population_factory.hpp"
#include "configuration/simulation_config.hpp"
#include "configuration/json_factory.hpp"

#include "../catch/catch.hpp"
#include "helpers.hpp"

#include <random>

using namespace epiabm;

TEST_CASE("sweeps/household_sweep: test initialize household_sweep", "[HouseholdSweep]")
{
    HouseholdSweepPtr subject = std::make_shared<HouseholdSweep>(
        std::make_shared<SimulationConfig>());
}

TEST_CASE("sweeps/household_sweep: test household_sweep bind_population", "[HouseholdSweep]")
{
    HouseholdSweepPtr subject = std::make_shared<HouseholdSweep>(
        std::make_shared<SimulationConfig>());
    PopulationPtr population = PopulationFactory().makePopulation(5, 5, 1000);
    bind_households(population, 500);
    population->initialize();
    REQUIRE_NOTHROW(subject->bind_population(population));
}

TEST_CASE("sweeps/household_sweep: test household_sweep run sweep", "[HouseholdSweep]")
{
    HouseholdSweepPtr subject = std::make_shared<HouseholdSweep>(
        JsonFactory().loadConfig(std::filesystem::path("../testdata/test_config.json")));
    PopulationPtr population = PopulationFactory().makePopulation(5, 5, 1000);
    bind_households(population, 500);
    random_seed(population, 10, InfectionStatus::InfectASympt, 5);
    population->initialize();
    REQUIRE_NOTHROW(subject->bind_population(population));
    for (int i = 0; i < 10; i++)
        REQUIRE_NOTHROW((*subject)(static_cast<unsigned short>(i)));
}

TEST_CASE("sweeps/household_sweep: test destructor", "[HouseholdSweep]")
{
    {
        SweepInterface* i = new HouseholdSweep(
            std::make_shared<SimulationConfig>());
        [[maybe_unused]] HouseholdSweep* subject = dynamic_cast<HouseholdSweep*>(i);
        delete i;
        i = nullptr;
        subject = nullptr;
    }
    {
        SweepInterface* i = new SweepInterface();
        i->operator()(0);
        delete i;
        i = nullptr;
    }
}


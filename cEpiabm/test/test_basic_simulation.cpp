
#include "simulations/basic_simulation.hpp"
#include "logfile.hpp"
#include "sweeps/random_seed_sweep.hpp"
#include "reporters/population_compartment_reporter.hpp"
#include "population_factory.hpp"
#include "configuration/json_factory.hpp"

#include "../catch/catch.hpp"

#include <random>
#include <iostream>

using namespace epiabm;

TEST_CASE("simulations/basic_simulation: test initialize basic_simulation", "[BasicSimulation]")
{
    LogFile::Instance()->configure(2, std::filesystem::path("output/basic_simulation/initialize.log"));

    PopulationFactory f = PopulationFactory();
    PopulationPtr population = f.makePopulation(10, 10, 100);
    population->initialize();
    BasicSimulation subject = BasicSimulation(population);
    REQUIRE_NOTHROW(subject.simulate(10));
}

TEST_CASE("simulations/basic_simulation: test addSweep", "[BasicSimulation]")
{
    LogFile::Instance()->configure(2, std::filesystem::path("output/basic_simulation/add_sweep.log"));
    PopulationFactory f = PopulationFactory();
    PopulationPtr population = f.makePopulation(10, 10, 100);
    population->initialize();
    BasicSimulation subject = BasicSimulation(population);

    REQUIRE_NOTHROW(subject.addSweep(std::make_shared<RandomSeedSweep>(
        JsonFactory().loadConfig(std::filesystem::path("../testdata/test_config.json")), 50)));
    REQUIRE_NOTHROW(subject.simulate(10));
}

TEST_CASE("simulations/basic_simulation: test addReporter", "[BasicSimulation]")
{
    LogFile::Instance()->configure(2, std::filesystem::path("output/basic_simulation/add_reporter.log"));
    PopulationFactory f = PopulationFactory();
    PopulationPtr population = f.makePopulation(10, 10, 100);
    population->initialize();
    BasicSimulation subject = BasicSimulation(population);

    REQUIRE_NOTHROW(subject.addTimestepReporter(
        std::make_shared<PopulationCompartmentReporter>("output/basic_simulation/population_output.csv")));
    REQUIRE_NOTHROW(subject.simulate(10));
}

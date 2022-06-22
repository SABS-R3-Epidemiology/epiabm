

#include "sweeps/spatial_sweep.hpp"
#include "population_factory.hpp"
#include "configuration/json_factory.hpp"

#include "../catch/catch.hpp"
#include "helpers.hpp"

#include <random>

using namespace epiabm;


TEST_CASE("sweeps/spatial_sweep: test initialize spatial_sweep", "[SpatialSweep]")
{
    SpatialSweepPtr subject = std::make_shared<SpatialSweep>(
        std::make_shared<SimulationConfig>());
}

TEST_CASE("sweeps/spatial_sweep: test spatial_sweep bind_population", "[SpatialSweep]")
{
    SpatialSweepPtr subject = std::make_shared<SpatialSweep>(
        std::make_shared<SimulationConfig>());
    PopulationPtr population = PopulationFactory().makePopulation(5, 5, 1000);
    population->initialize();
    REQUIRE_NOTHROW(subject->bind_population(population));
}

TEST_CASE("sweeps/spatial_sweep: test spatial_sweep with no cells", "[SpatialSweep]")
{
    SpatialSweepPtr subject = std::make_shared<SpatialSweep>(
        std::make_shared<SimulationConfig>());
    PopulationPtr population = PopulationFactory().makePopulation(0, 1, 1);
    population->initialize();
    REQUIRE_NOTHROW(subject->bind_population(population));
    REQUIRE_NOTHROW((*subject)(static_cast<unsigned short>(0)));
}

TEST_CASE("sweeps/spatial_sweep: test spatial_sweep with no infectors", "[SpatialSweep]")
{
    SpatialSweepPtr subject = std::make_shared<SpatialSweep>(
        std::make_shared<SimulationConfig>());
    PopulationPtr population = PopulationFactory().makePopulation(5, 1, 0);
    population->initialize();
    REQUIRE_NOTHROW(subject->bind_population(population));
    REQUIRE_NOTHROW((*subject)(static_cast<unsigned short>(0)));
}

TEST_CASE("sweeps/spatial_sweep: test spatial_sweep run sweep", "[SpatialSweep]")
{
    SpatialSweepPtr subject = std::make_shared<SpatialSweep>(
        JsonFactory().loadConfig(std::filesystem::path("../testdata/test_config.json")));
    PopulationPtr population = PopulationFactory().makePopulation(5, 5, 1000);
    random_seed(population, 10, InfectionStatus::InfectASympt, 5);
    population->initialize();
    REQUIRE_NOTHROW(subject->bind_population(population));
    for (size_t i = 0; i < 10; i++)
        REQUIRE_NOTHROW((*subject)(static_cast<unsigned short>(i)));
}

TEST_CASE("sweeps/spatial_sweep: test spatial_sweep run sweep without ages", "[SpatialSweep]")
{
    SimulationConfigPtr cfg = JsonFactory().loadConfig(std::filesystem::path("../testdata/test_config.json"));
    cfg->infectionConfig->hostProgressionConfig->use_ages = true;
    SpatialSweepPtr subject = std::make_shared<SpatialSweep>(cfg);
    PopulationPtr population = PopulationFactory().makePopulation(5, 5, 1000);
    random_seed(population, 10, InfectionStatus::InfectASympt, 5);
    population->initialize();
    REQUIRE_NOTHROW(subject->bind_population(population));
    for (size_t i = 0; i < 10; i++)
        REQUIRE_NOTHROW((*subject)(static_cast<unsigned short>(i)));
}

TEST_CASE("sweeps/spatial_sweep: test spatial_sweep run sweep invalid distance metric", "[SpatialSweep]")
{
    SimulationConfigPtr cfg = JsonFactory().loadConfig(std::filesystem::path("../testdata/test_config.json"));
    cfg->infectionConfig->spatial_distance_metric = "invalid distance metric";
    SpatialSweepPtr subject = std::make_shared<SpatialSweep>(cfg);
    PopulationPtr population = PopulationFactory().makePopulation(5, 5, 1000);
    random_seed(population, 10, InfectionStatus::InfectASympt, 5);
    population->initialize();
    REQUIRE_NOTHROW(subject->bind_population(population));
    for (size_t i = 0; i < 10; i++)
        REQUIRE_THROWS((*subject)(static_cast<unsigned short>(i)));
}


TEST_CASE("sweeps/spatial_sweep: test spatial_sweep run sweep covidsim distance metric", "[SpatialSweep]")
{
    SimulationConfigPtr cfg = JsonFactory().loadConfig(std::filesystem::path("../testdata/test_config.json"));
    cfg->infectionConfig->spatial_distance_metric = "covidsim";
    SpatialSweepPtr subject = std::make_shared<SpatialSweep>(cfg);
    PopulationPtr population = PopulationFactory().makePopulation(5, 5, 1000);
    random_seed(population, 10, InfectionStatus::InfectASympt, 5);
    population->initialize();
    REQUIRE_NOTHROW(subject->bind_population(population));
    for (size_t i = 0; i < 10; i++)
        REQUIRE_NOTHROW((*subject)(static_cast<unsigned short>(i)));
}

TEST_CASE("sweeps/spatial_sweep: test destructor", "[SpatialSweep]")
{
    {
        SweepInterface *i = new SpatialSweep(
            std::make_shared<SimulationConfig>());
        [[maybe_unused]] SpatialSweep *subject = dynamic_cast<SpatialSweep *>(i);
        delete i;
        i = nullptr;
        subject = nullptr;
    }
    {
        SweepInterface *i = new SweepInterface();
        i->operator()(0);
        delete i;
        i = nullptr;
    }
}



#include "sweeps/new_infection_sweep.hpp"
#include "population_factory.hpp"
#include "configuration/json_factory.hpp"

#include "../catch/catch.hpp"
#include "helpers.hpp"

#include <random>

using namespace epiabm;

inline void enqueueRandom(PopulationPtr population)
{
    for (size_t c = 0; c < population->cells().size(); c++)
    {
        Cell* cell = &population->cells()[c];
        for (size_t mc = 0; mc < cell->microcells().size(); mc++)
        {
            for (size_t p = 0; p < cell->people().size(); p++)
            {
                if (std::rand() % 100 < 10)
                {
                    cell->enqueuePerson(p);
                }
            }
        }
    }
}

TEST_CASE("sweeps/new_infection_sweep: test initialize new_infection_sweep", "[NewInfectionSweep]")
{
    NewInfectionSweepPtr subject = std::make_shared<NewInfectionSweep>(
        std::make_shared<SimulationConfig>());
}

TEST_CASE("sweeps/new_infection_sweep: test new_infection_sweep bind_population", "[NewInfectionSweep]")
{
    NewInfectionSweepPtr subject = std::make_shared<NewInfectionSweep>(
        std::make_shared<SimulationConfig>());
    PopulationPtr population = PopulationFactory().makePopulation(5, 5, 1000);
    population->initialize();
    REQUIRE_NOTHROW(subject->bind_population(population));
}

TEST_CASE("sweeps/new_infection_sweep: test new_infection_sweep run sweep", "[NewInfectionSweep]")
{
    NewInfectionSweepPtr subject = std::make_shared<NewInfectionSweep>(
        JsonFactory().loadConfig(std::filesystem::path("../testdata/test_config.json")));
    PopulationPtr population = PopulationFactory().makePopulation(5, 5, 1000);
    enqueueRandom(population);
    population->initialize();
    REQUIRE_NOTHROW(subject->bind_population(population));
    for (int i = 0; i < 10; i++)
        REQUIRE_NOTHROW((*subject)(static_cast<unsigned short>(i)));
}

TEST_CASE("sweeps/new_infection_sweep: test destructor", "[NewInfectionSweep]")
{
    {
        SweepInterface* i = new NewInfectionSweep(
            std::make_shared<SimulationConfig>());
        [[maybe_unused]] NewInfectionSweep* subject = dynamic_cast<NewInfectionSweep*>(i);
        delete i;
        i = nullptr;
        subject = nullptr;
    }
}

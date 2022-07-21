

#include "dataclasses/cell.hpp"
#include "sweeps/spatial_sweep.hpp"
#include "population_factory.hpp"

#include "../catch/catch.hpp"
#include "helpers.hpp"

#include <random>

using namespace epiabm;


TEST_CASE("sweeps/spatial_sweep: test initialize spatial_sweep", "[SpatialSweep]")
{
    SpatialSweepPtr subject = std::make_shared<SpatialSweep>();
}

TEST_CASE("sweeps/spatial_sweep: test spatial_sweep bind_population", "[SpatialSweep]")
{
    SpatialSweepPtr subject = std::make_shared<SpatialSweep>();
    PopulationPtr population = PopulationFactory().makePopulation(5, 5, 1000);
    population->initialize();
    REQUIRE_NOTHROW(subject->bind_population(population));
}

TEST_CASE("sweeps/spatial_sweep: test spatial_sweep with no cells", "[SpatialSweep]")
{
    SpatialSweepPtr subject = std::make_shared<SpatialSweep>();
    PopulationPtr population = PopulationFactory().makePopulation(0, 1, 1);
    population->initialize();
    REQUIRE_NOTHROW(subject->bind_population(population));
    REQUIRE_NOTHROW((*subject)(static_cast<unsigned short>(0)));
}

TEST_CASE("sweeps/spatial_sweep: test spatial_sweep with no infectors", "[SpatialSweep]")
{
    SpatialSweepPtr subject = std::make_shared<SpatialSweep>();
    PopulationPtr population = PopulationFactory().makePopulation(5, 1, 0);
    population->initialize();
    REQUIRE_NOTHROW(subject->bind_population(population));
    REQUIRE_NOTHROW((*subject)(static_cast<unsigned short>(0)));
}

TEST_CASE("sweeps/spatial_sweep: test spatial_sweep run sweep", "[SpatialSweep]")
{
    SpatialSweepPtr subject = std::make_shared<SpatialSweep>();
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
        SweepInterface *i = new SpatialSweep();
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

TEST_CASE("sweeps/spatial_sweep: test call", "[SpatialSweep]")
{   
    {   
        std::cout << "here";
        SpatialSweepPtr subject = std::make_shared<SpatialSweep>();
        PopulationFactory pop_fact = PopulationFactory();
        PopulationPtr one_cell_pop = pop_fact.makePopulation(1, 1, 1);
        one_cell_pop->initialize();
        subject->bind_population(one_cell_pop);
        // Only one cell
        REQUIRE_NOTHROW((*subject)(1));

        // Two cells, one initially empty
        PopulationPtr two_cell_pop = pop_fact.makePopulation(2, 1, 0);
        pop_fact.addPeople(&two_cell_pop->cells()[0], 0, 1);
        two_cell_pop->initialize();
        subject->bind_population(two_cell_pop);
        REQUIRE_NOTHROW((*subject)(1));

        // Initially no infectors
        Cell* cellinf = &two_cell_pop->cells()[0];
        cellinf->people()[0].updateStatus(cellinf, InfectionStatus::InfectMild, 1);
        two_cell_pop->initialize();
        subject->bind_population(two_cell_pop);
        REQUIRE_NOTHROW((*subject)(1));

        // make first person infectious
        // sweep runs normally
        PopulationPtr normal_pop = pop_fact.makePopulation(2, 1, 1);
        cellinf = &normal_pop->cells()[0];
        cellinf->people()[0].updateStatus(cellinf, InfectionStatus::InfectMild, 1);
        normal_pop->initialize();
        subject->bind_population(normal_pop);
        REQUIRE_NOTHROW((*subject)(1));

        // make all infectious
        Cell* cellsus = &normal_pop->cells()[0];
        cellsus->people()[0].updateStatus(cellinf, InfectionStatus::InfectMild, 1);
        normal_pop->initialize();
        subject->bind_population(normal_pop);
        REQUIRE_NOTHROW((*subject)(1));
    }
}

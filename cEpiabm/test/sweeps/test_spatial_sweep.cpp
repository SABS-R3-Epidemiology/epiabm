

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
{   //can i test inline functions?
    {   
        SpatialSweepPtr subject = std::make_shared<SpatialSweep>();
        PopulationPtr population = PopulationFactory().makePopulation(2, 1, 1000);
        // make first person infectious
        Cell* cell1 = &population->cells()[0];
        cell1->people()[0].updateStatus(cell1, InfectionStatus::InfectMild, static_cast<unsigned short>(1));

        population->initialize();



    }
}

TEST_CASE("sweeps/spatial_sweep: test cell", "[SpatialSweep]")
{   //can i even test inline functions?
    {   
        Cell cell1 = Cell(0);
        Cell cell2 = Cell(0);
        cell1.setLocation(std::make_pair(1.0, 0.0));

        std::vector<Cell> cells = {cell1, cell2};//want a vector of pointers to cells
        auto weights = getWeightsFromCells(cells, cell1);

        std::vector<double> test_weights = {0, 1};
        REQUIRE(weights=test_weights);

        // now test with the doCovidsim flag
        // need to add infectious person to cell2
        cell2.addMember(1);
        weights = SpatialSweep::getWeightsFromCells(cells, cell1, false, true);
        
    }
}
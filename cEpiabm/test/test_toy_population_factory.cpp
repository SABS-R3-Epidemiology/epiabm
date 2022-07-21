
#include "toy_population_factory.hpp"
#include "dataclasses/population.hpp"
#include "dataclasses/cell.hpp"
#include "dataclasses/microcell.hpp"
#include "dataclasses/person.hpp"

#include "catch/catch.hpp"

using namespace epiabm;

TEST_CASE("toy_population_factory: test make empty population", "[ToyPopulationFactory]")
{
    ToyPopulationFactory factory = ToyPopulationFactory();
    PopulationPtr population = factory.makePopulation(0,0,0,0,0);

    REQUIRE(population->cells().empty());
}

inline void testMakePopulation(size_t nPeople, size_t nCells, size_t nMicrocells, size_t nHouseholds, size_t nPlaces)
{
    ToyPopulationFactory factory = ToyPopulationFactory();
    PopulationPtr pop = factory.makePopulation(
        nPeople, nCells, nMicrocells, nHouseholds, nPlaces);
    
    REQUIRE(pop->cells().size() == nCells);
    size_t peopleCount = 0;
    for (size_t ci = 0; ci < pop->cells().size(); ci++)
    {
        Cell& cell = pop->cells()[ci];
        peopleCount += cell.people().size();

        for (size_t pi = 0; pi < cell.people().size(); pi++)
        {
            Person& p = cell.people()[pi];
            REQUIRE(p.cellPos() == pi);
        }

        size_t microcellPeopleCount = 0;;
        for (size_t mi = 0; mi < cell.microcells().size(); mi++)
        {
            Microcell& microcell = cell.microcells()[mi];
            microcellPeopleCount += microcell.people().size();

            for (size_t pi = 0; pi < microcell.people().size(); pi++)
            {
                Person& p = cell.people()[microcell.people()[pi]];
                REQUIRE(p.microcellPos() == pi);
                REQUIRE(p.microcell() == mi);
            }

            REQUIRE(microcell.households().size() == nHouseholds);
            for (size_t hi = 0; hi < microcell.households().size(); hi++)
            {
                HouseholdPtr household = microcell.households()[hi];
                for (auto& pi : household->members())
                {
                    Person& p = microcell.getPerson(cell, pi);
                    REQUIRE(p.household() == hi);
                }
            }
        }
        REQUIRE(microcellPeopleCount == cell.people().size());
    }
    REQUIRE(peopleCount == nPeople);
}

TEST_CASE("toy_population_factory: test make population", "[ToyPopulationFactory]")
{
    testMakePopulation(100, 10, 1, 0, 0);
    testMakePopulation(5000, 200, 1, 5, 100);
}

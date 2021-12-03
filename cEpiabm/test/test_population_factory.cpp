
#include "population_factory.hpp"
#include "dataclasses/population.hpp"
#include "dataclasses/cell.hpp"
#include "dataclasses/microcell.hpp"
#include "dataclasses/person.hpp"

#include <catch2/catch_test_macros.hpp>

using namespace epiabm;

TEST_CASE("population_factory: test make empty population", "[PopulationFactory]")
{
    PopulationFactory factory = PopulationFactory();
    PopulationPtr population = factory.makePopulation();

    REQUIRE(population->cells().empty());
}

TEST_CASE("population_factory: test add cell", "[PopulationFactory]")
{
    PopulationFactory factory = PopulationFactory();
    PopulationPtr population = factory.makePopulation();
    REQUIRE(population->cells().empty());

    factory.addCell(population);
    REQUIRE(population->cells().empty() == false);
    REQUIRE(population->cells().size() == 1);

    for (int i = 0; i < 4; i++)
        factory.addCell(population);
    REQUIRE(population->cells().size() == 5);
}

TEST_CASE("population_factory: test add cells", "[PopulationFactory]")
{
    PopulationFactory factory = PopulationFactory();
    PopulationPtr population = factory.makePopulation();
    REQUIRE(population->cells().empty());

    factory.addCells(population, 1);
    REQUIRE(population->cells().empty() == false);
    REQUIRE(population->cells().size() == 1);

    factory.addCells(population, 4);
    REQUIRE(population->cells().size() == 5);
}

TEST_CASE("population_factory: test add microcell", "[PopulationFactory]")
{
    PopulationFactory factory = PopulationFactory();
    PopulationPtr population = factory.makePopulation();
    REQUIRE(population->cells().empty());

    factory.addCell(population);
    REQUIRE(population->cells().size() == 1);

    factory.addMicrocell(&population->cells()[0]);
    REQUIRE(population->cells().size() == 1);
    REQUIRE(population->cells()[0].microcells().size() == 1);

    for (int i = 0; i < 4; i++)
        factory.addMicrocell(&population->cells()[0]);
    REQUIRE(population->cells().size() == 1);
    REQUIRE(population->cells()[0].microcells().size() == 5);
}

TEST_CASE("population_factory: test add microcells", "[PopulationFactory]")
{
    PopulationFactory factory = PopulationFactory();
    PopulationPtr population = factory.makePopulation();
    REQUIRE(population->cells().empty());

    factory.addCell(population);
    REQUIRE(population->cells().size() == 1);

    factory.addMicrocells(&population->cells()[0], 1);
    REQUIRE(population->cells().size() == 1);
    REQUIRE(population->cells()[0].microcells().size() == 1);

    factory.addMicrocells(&population->cells()[0], 4);
    REQUIRE(population->cells().size() == 1);
    REQUIRE(population->cells()[0].microcells().size() == 5);
}

TEST_CASE("population_factory: test add person", "[PopulationFactory]")
{
    PopulationFactory factory = PopulationFactory();
    PopulationPtr population = factory.makePopulation();
    factory.addCell(population);
    factory.addMicrocells(&population->cells()[0], 5);

    factory.addPerson(&population->cells()[0], &population->cells()[0].microcells()[0]);
    REQUIRE(population->cells()[0].people().size() == 1);
    for (size_t i = 0; i < 5; i++)
        REQUIRE(population->cells()[0].microcells()[i].people().size() == ((i == 0) ? 1 : 0));

    for (size_t i = 1; i < 5; i++)
    {
        for (size_t j = 0; j <= i; j++)
        {
            factory.addPerson(&population->cells()[0], &population->cells()[0].microcells()[i]);
        }
    }
    REQUIRE(population->cells()[0].people().size() == 15);
    for (size_t i = 0; i < 5; i++)
    {
        REQUIRE(population->cells()[0].microcells()[i].people().size() == i + 1);
    }
}

TEST_CASE("population_factory: test add people", "[PopulationFactory]")
{
    PopulationFactory factory = PopulationFactory();
    PopulationPtr population = factory.makePopulation();
    factory.addCell(population);
    factory.addMicrocells(&population->cells()[0], 5);

    factory.addPeople(&population->cells()[0], &population->cells()[0].microcells()[0], 1);
    REQUIRE(population->cells()[0].people().size() == 1);
    for (size_t i = 0; i < 5; i++)
        REQUIRE(population->cells()[0].microcells()[i].people().size() == ((i == 0) ? 1 : 0));

    for (size_t i = 1; i < 5; i++)
    {
        factory.addPeople(&population->cells()[0], &population->cells()[0].microcells()[i], i + 1);
    }
    REQUIRE(population->cells()[0].people().size() == 15);
    for (size_t i = 0; i < 5; i++)
    {
        REQUIRE(population->cells()[0].microcells()[i].people().size() == i + 1);
    }
}

TEST_CASE("population_factory: test make population", "[PopulationFactory]")
{
    PopulationFactory factory = PopulationFactory();

    auto test = [&](std::string name, size_t n_cells, size_t n_microcells, size_t n_people)
    {
        SECTION(name)
        {
            PopulationPtr p = factory.makePopulation(n_cells, n_microcells, n_people);
            REQUIRE(p->cells().size() == n_cells);
            for (size_t i = 0; i < n_cells; i++)
            {
                REQUIRE(p->cells()[i].microcells().size() == n_microcells);
                REQUIRE(p->cells()[i].people().size() == n_microcells * n_people);
                for (size_t j = 0; j < n_microcells; j++)
                {
                    REQUIRE(p->cells()[i].microcells()[j].people().size() == n_people);
                }
            }
        }
    };

    SECTION("Cells")
    {
        test("tiny", 1, 0, 0);
        test("small", 5, 0, 0);
        test("medium", 50, 0, 0);
    }

    SECTION("Cells,Microcells")
    {
        test("tiny", 1, 1, 0);
        test("small", 1, 5, 0);
        test("medium", 5, 5, 0);
        test("large", 10, 50, 0);
    }

    SECTION("Cells,Microcells,People")
    {
        test("tiny", 1, 1, 1);
        test("small", 1, 1, 5);
        test("small2", 1, 5, 5);
        test("medium", 5, 5, 5);
        test("large", 5, 10, 50);
    }
}

TEST_CASE("population_factory: test make large population", "[PopulationFactory]")
{
    PopulationFactory factory = PopulationFactory();

    auto test = [&](std::string name, size_t n_cells, size_t n_microcells, size_t n_people)
    {
        SECTION(name)
        {
            PopulationPtr p = factory.makePopulation(n_cells, n_microcells, n_people);
            REQUIRE(p->cells().size() == n_cells);
            for (size_t i = 0; i < n_cells; i++)
            {
                REQUIRE(p->cells()[i].microcells().size() == n_microcells);
                REQUIRE(p->cells()[i].people().size() == n_microcells * n_people);
            }
        }
    };

    test("10x10x100", 10, 10, 100);
    test("10x100x1000", 10, 100, 1000);
    test("100x100x1000", 100, 100, 1000);
    test("1000x100x1000", 1000, 100, 100);
}

TEST_CASE("dataclasses/population_factory: test position links", "[PopulationFactory]")
{
    PopulationFactory factory = PopulationFactory();

    auto test = [&](std::string name, size_t n_cells, size_t n_microcells, size_t n_people)
    {
        SECTION(name)
        {
            PopulationPtr p = factory.makePopulation(n_cells, n_microcells, n_people);
            REQUIRE(p->cells().size() == n_cells);
            for (size_t i = 0; i < n_cells; i++)
            {
                REQUIRE(p->cells()[i].microcells().size() == n_microcells);
                REQUIRE(p->cells()[i].people().size() == n_microcells * n_people);

                for (size_t j = 0; j < n_microcells; j++)
                {
                    REQUIRE(p->cells()[i].microcells()[j].people().size() == n_people);
                    REQUIRE(p->cells()[i].microcells()[j].cellPos() == j);
                    for (size_t k = 0; k < n_people; k++)
                    {
                        REQUIRE(p->cells()[i].microcells()[j].getPerson(p->cells()[i], k).microcellPos() == k);
                    }
                }

                for (size_t k = 0; k < n_microcells * n_people; k++)
                {
                    REQUIRE(p->cells()[i].people()[k].cellPos() == k);
                }
            }
        }
    };

    test("small", 1, 1, 5);
    test("small2", 1, 5, 5);
    test("medium", 5, 5, 5);
    test("large", 5, 10, 50);
}

TEST_CASE("dataclasses/population_factory: test microcell initialization", "[Microcell][PopulationFactory]")
{
    PopulationFactory f = PopulationFactory();
    PopulationPtr p = f.makePopulation(1, 5, 10);
    for (size_t i = 0; i < p->cells()[0].microcells().size(); i++)
    {
        for (size_t j = 0; j < p->cells()[0].microcells()[i].people().size(); j++)
        {
            Person subject = p->cells()[0].microcells()[i].getPerson(p->cells()[0], j);
            REQUIRE(subject.microcellPos() == j);
        }
    }
}


#include "dataclasses/population.hpp"
#include "dataclasses/cell.hpp"

#include <catch2/catch_test_macros.hpp>

using namespace epiabm;

TEST_CASE("dataclasses/population: test initialize population", "[Population]")
{
    Population subject = Population();
    REQUIRE(subject.cells().size() == 0);
}

TEST_CASE("dataclasses/population: test add cells", "[Population]")
{
    Population subject = Population();
    REQUIRE(subject.cells().empty());

    for (size_t i = 0; i < 1000; i++)
    {
        subject.cells().push_back(Cell());
    }
    REQUIRE(subject.cells().size() == 1000);
}

TEST_CASE("dataclasses/population: test forEachCell", "[Population]")
{
    Population subject = Population();
    std::set<Cell*> cells = std::set<Cell*>();

    subject.cells().reserve(1000);
    for (size_t i = 0; i < 1000; i++)
    {
        subject.cells().push_back(Cell());
        cells.insert(&subject.cells()[i]);
    }
    REQUIRE(subject.cells().size() == 1000);
    REQUIRE(cells.size() == 1000);

    REQUIRE_NOTHROW(
        subject.forEachCell(
            [&](Cell *cell)
            {
                REQUIRE(cells.find(cell) != cells.end());
                cells.erase(cell);
                return true;
            }));
    REQUIRE(cells.size() == 0);
}

TEST_CASE("dataclasses/population: test forEachCell early stop", "[Population]")
{
    Population subject = Population();
    std::set<Cell*> cells = std::set<Cell*>();

    subject.cells().reserve(1000);
    for (size_t i = 0; i < 1000; i++)
    {
        subject.cells().push_back(Cell());
        cells.insert(&subject.cells()[i]);
    }
    REQUIRE(subject.cells().size() == 1000);
    REQUIRE(cells.size() == 1000);

    int ctr = 0;
    REQUIRE_NOTHROW(
        subject.forEachCell(
            [&](Cell *cell)
            {
                REQUIRE(cells.find(cell) != cells.end());
                cells.erase(cell);
                ctr++;
                return ctr < 500;
            }));
    REQUIRE(cells.size() == 500);
}

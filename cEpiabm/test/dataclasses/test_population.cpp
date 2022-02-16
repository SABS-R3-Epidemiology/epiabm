
#include "dataclasses/population.hpp"
#include "dataclasses/cell.hpp"

#include "../catch/catch.hpp"

using namespace epiabm;

TEST_CASE("dataclasses/population: test initialize population", "[Population]")
{
    Population subject = Population();
    REQUIRE(subject.cells().size() == 0);
    REQUIRE(subject.places().empty());
}

TEST_CASE("dataclasses/population: test add cells", "[Population]")
{
    Population subject = Population();
    REQUIRE(subject.cells().empty());

    for (size_t i = 0; i < 1000; i++)
    {
        subject.cells().push_back(Cell(subject.cells().size()));
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
        subject.cells().push_back(Cell(subject.cells().size()));
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
        subject.cells().push_back(Cell(subject.cells().size()));
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

TEST_CASE("dataclasses/population: test forEachPlace", "[Population]")
{
    Population subject = Population();
    std::set<Place*> places = std::set<Place*>();
    for (size_t i = 0; i < 100; i++)
    {
        subject.places().push_back(Place(i));
    }
    for (size_t i = 0; i < 100; i++) 
    {
        places.insert(&subject.places()[i]);
    }
    REQUIRE(subject.places().size() == 100);

    subject.forEachPlace(
        [&](Place* place)
        {
            REQUIRE(places.find(place) != places.end());
            places.erase(place);
            return true;
        }
    );
    REQUIRE(places.size() == 0);
}


TEST_CASE("dataclasses/population: test forEachPlace early stop", "[Population]")
{
    Population subject = Population();
    std::set<Place*> places = std::set<Place*>();
    for (size_t i = 0; i < 100; i++)
    {
        subject.places().push_back(Place(i));
    }
    for (size_t i = 0; i < 100; i++) 
    {
        places.insert(&subject.places()[i]);
        REQUIRE(subject.places()[i].populationPos() == i);
    }
    REQUIRE(subject.places().size() == 100);

    int ctr = 0;
    subject.forEachPlace(
        [&](Place* place)
        {
            REQUIRE(places.find(place) != places.end());
            places.erase(place);
            ctr++;
            return ctr < 50;
        }
    );
    REQUIRE(places.size() == 50);
}


#include "dataclasses/microcell.hpp"
#include "dataclasses/cell.hpp"
#include "dataclasses/place.hpp"

#include <catch2/catch_test_macros.hpp>

using namespace epiabm;

TEST_CASE("dataclasses/microcell: test initialize microcell", "[Microcell]")
{
    Microcell subject = Microcell(5);
    REQUIRE(subject.cellPos() == 5);
    REQUIRE(subject.people().empty());
    REQUIRE(subject.places().empty());
}

TEST_CASE("dataclasses/microcell: test forEachPerson", "[Microcell]")
{
    Cell cell = Cell();
    cell.microcells().push_back(Microcell(0));
    
    std::set<Person*> peopleSet;
    for (size_t i = 0; i < 100; i++)
    {
        cell.people().push_back(Person(0, i));
    }
    for (size_t i = 0; i < 100; i++)
    {
        peopleSet.insert(&cell.people()[i]);
        cell.microcells()[0].people().push_back(i);
    }
    REQUIRE(cell.microcells()[0].people().size() == 100);

    REQUIRE_NOTHROW(
        cell.microcells()[0].forEachPerson(cell,
            [&](Person *p)
            {
                peopleSet.erase(p);
                return true;
            }));
    REQUIRE(peopleSet.size() == 0);
}

TEST_CASE("dataclasses/microcell: test forEachPerson early stop", "[Microcell]")
{
    Cell cell = Cell();
    cell.microcells().push_back(Microcell(0));
    std::set<Person *> peopleSet;
    for (size_t i = 0; i < 100; i++)
    {
        cell.people().push_back(Person(0, i));
    }
    for (size_t i = 0; i < 100; i++)
    {
        peopleSet.insert(&cell.people()[i]);
        cell.microcells()[0].people().push_back(i);
    }
    REQUIRE(cell.microcells()[0].people().size() == 100);

    int ctr = 0;
    REQUIRE_NOTHROW(
        cell.microcells()[0].forEachPerson(
            cell,
            [&](Person *p)
            {
                peopleSet.erase(p);
                ctr++;
                return ctr < 50;
            }));
    REQUIRE(peopleSet.size() == 50);
}

TEST_CASE("dataclasses/microcell: test forEachPlace", "[Microcell]")
{
    Microcell subject = Microcell(5);
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

TEST_CASE("dataclasses/microcell: test forEachPlace early stop", "[Microcell]")
{
    Microcell subject = Microcell(5);
    std::set<Place*> places = std::set<Place*>();
    for (size_t i = 0; i < 100; i++)
    {
        subject.places().push_back(Place(i));
    }
    for (size_t i = 0; i < 100; i++) 
    {
        places.insert(&subject.places()[i]);
        REQUIRE(subject.places()[i].microcellPos() == i);
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

TEST_CASE("dataclasses/microcell: test getPerson", "[Microcell]")
{
    Cell cell = Cell();
    cell.microcells().push_back(Microcell(0));
    for (size_t i = 0; i < 100; i++)
    {
        cell.people().push_back(Person(0, i));
    }
    for (size_t i = 0; i < 100; i++)
    {
        cell.microcells()[0].people().push_back(i);
    }
    REQUIRE(cell.microcells()[0].people().size() == 100);

    for (size_t i = 0; i < 100; i++)
    {
        REQUIRE(cell.microcells()[0].getPerson(cell, i).microcellPos() == i);
    }
}

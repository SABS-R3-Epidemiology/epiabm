
#include "dataclasses/microcell.hpp"
#include "dataclasses/cell.hpp"
#include "dataclasses/place.hpp"

#include "../catch/catch.hpp"

using namespace epiabm;

TEST_CASE("dataclasses/microcell: test initialize microcell", "[Microcell]")
{
    Microcell subject = Microcell(5);
    REQUIRE(subject.cellPos() == 5);
    REQUIRE(subject.people().empty());
}

TEST_CASE("dataclasses/microcell: test forEachPerson", "[Microcell]")
{
    Cell cell = Cell(0);
    cell.microcells().push_back(Microcell(0));
    
    std::set<Person*> peopleSet;
    for (size_t i = 0; i < 100; i++)
    {
        cell.people().push_back(Person(0, 0, i));
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
    Cell cell = Cell(0);
    cell.microcells().push_back(Microcell(0));
    std::set<Person *> peopleSet;
    for (size_t i = 0; i < 100; i++)
    {
        cell.people().push_back(Person(0, 0, i));
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

TEST_CASE("dataclasses/microcell: test getPerson", "[Microcell]")
{
    Cell cell = Cell(0);
    cell.microcells().push_back(Microcell(0));
    for (size_t i = 0; i < 100; i++)
    {
        cell.people().push_back(Person(0, 0, i));
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

TEST_CASE("dataclasses/microcell: test getHouseholds", "[Microcell]")
{
    Cell cell = Cell(0);
    cell.microcells().push_back(Microcell(0));
    for (size_t i = 0; i < 100; i++)
    {
        cell.people().push_back(Person(0, 0, i));
    }
    for (size_t i = 0; i < 100; i++)
    {
        cell.microcells()[0].households().push_back(
            std::make_shared<Household>(i));
    }
    REQUIRE(cell.microcells()[0].households().size() == 100);

    for (size_t i = 0; i < 100; i++)
    {
        REQUIRE(cell.microcells()[0].getHousehold(i)->microcellPos() == i);
    }
}

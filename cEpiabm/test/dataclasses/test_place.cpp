
#include "dataclasses/population.hpp"
#include "dataclasses/place.hpp"

#include "../catch/catch.hpp"

#include <random>
#include <iostream>

using namespace epiabm;

inline Population makeSubjectPlaceTest(size_t n_places, size_t n_cells, size_t n_people)
{
    Population subject = Population();
    subject.cells().reserve(n_cells);
    subject.places().reserve(n_places);
    for (size_t i = 0; i < n_places; i++)
    {
        subject.places().push_back(Place(i));
    }
    for (size_t i = 0; i < n_cells; i++)
    {
        subject.cells().push_back(std::make_shared<Cell>(i));
        subject.cells()[i]->people().reserve(n_people);
        for (size_t j = 0; j < n_people; j++)
        {
            subject.cells()[i]->people().push_back(Person(i, j, j));

            /*printf("Microcell: %ld, Person: (%ld, %ld)\n",
                i,
                subject.people()[subject.microcells()[i].people()[j]].cellPos(),
                subject.people()[subject.microcells()[i].people()[j]].microcellPos());//*/
        }
    }
    return subject;
}

TEST_CASE("dataclasses/place: test initialize place", "[Place]")
{
    Place subject = Place(5);
    REQUIRE(subject.populationPos() == 5);
}


TEST_CASE("dataclasses/place: test add member", "[Place]")
{
    Place subject = Place(5);
    REQUIRE(subject.populationPos() == 5);

    REQUIRE(subject.members().empty());

    std::set<std::pair<size_t, size_t>> members = std::set<std::pair<size_t, size_t>>();
    for (int i = 0; i < 100000; i++)
    {
        size_t newMember = static_cast<size_t>(std::rand() % 100000);
        REQUIRE(subject.addMember(0, newMember) == (members.find({ 0, newMember }) == members.end()));
        members.insert({ 0, newMember });
    }
}

TEST_CASE("dataclasses/place: test add member already exists", "[Place]")
{
    Place subject = Place(5);
    REQUIRE(subject.populationPos() == 5);

    REQUIRE(subject.members().empty());

    std::set<std::pair<size_t, size_t>> members = std::set<std::pair<size_t, size_t>>();
    for (int i = 0; i < 1000000; i++)
    {
        size_t newMember = static_cast<size_t>(std::rand() % 1000);
        REQUIRE(subject.addMember(0, newMember) == (members.find({ 0, newMember }) == members.end()));
        members.insert({ 0, newMember });
    }

    for (size_t i = 0; i < 1000000; i++)
    {
        REQUIRE(subject.isMember(0, i) == (members.find({ 0, i }) != members.end()));
    }
}

inline void forEachMemberTestPlace(size_t n_places, size_t n_cells, size_t n_people)
{
    std::vector<std::set<Person*>> members = std::vector<std::set<Person*>>(n_places);

    Population subject = makeSubjectPlaceTest(n_places, n_cells, n_people);

    //std::cout << "Num Cells: " << subject.cells().size() << std::endl;
    for (size_t c = 0; c < subject.cells().size(); c++)
    {
        //std::cout << "Num People: " << subject.cells()[c].people().size() << std::endl;
        for (size_t p = 0; p < subject.cells()[c]->people().size(); p++)
        {
            for (size_t i = 0; i < n_places; i++)
            {
                if (std::rand() % 100 > 90) continue;
                REQUIRE(subject.places()[i].addMember(c, p));
                members[i].insert(&subject.cells()[c]->people()[p]);
                subject.cells()[c]->people()[p].places().insert(i);
            }
        }
    }

    for (size_t i = 0; i < subject.places().size(); i++)
    {
        auto callback = [&](Person* p)
        {
            REQUIRE(p->places().find(i) != p->places().end());
            REQUIRE(members[i].find(p) != members[i].end());
            members[i].erase(p);
            return true;
        };

        REQUIRE_NOTHROW(subject.places()[i].forEachMember(
            subject, callback));

        REQUIRE(members[i].size() == 0);
    }

    for (size_t i = 0; i < subject.places().size(); i++)
    {
        size_t ctr = 0;
        auto callback = [&](Person* p)
        {
            REQUIRE(members[i].find(p) == members[i].end());
            members[i].insert(p);
            ctr++;
            return rand() % 100 < 90;
        };

        REQUIRE_NOTHROW(subject.places()[i].forEachMember(
            subject, callback));

        REQUIRE(members[i].size() == ctr);
    }
}

TEST_CASE("dataclasses/place: test forEachMember Small", "[Place]")
{
    forEachMemberTestPlace(1, 1, 1000);
    forEachMemberTestPlace(1, 10, 1000);
    forEachMemberTestPlace(1, 100, 1000);
}

TEST_CASE("dataclasses/place: test forEachMember Medium", "[Place]")
{
    forEachMemberTestPlace(2, 5, 10);
    forEachMemberTestPlace(10, 10, 1000);
}

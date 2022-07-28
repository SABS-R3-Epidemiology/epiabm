#include "dataclasses/person.hpp"
#include "dataclasses/cell.hpp"
#include "dataclasses/population.hpp"

#include "../catch/catch.hpp"

using namespace epiabm;

TEST_CASE("dataclasses/person: test initialize person", "[Person]")
{
    Person subject = Person(0,5, 10);
    REQUIRE(subject.cellPos() == 5);
    REQUIRE(subject.microcellPos() == 10);
    REQUIRE(subject.microcell() == 0);
    REQUIRE_NOTHROW(subject.params());
    REQUIRE(subject.status() == InfectionStatus::Susceptible);
}

TEST_CASE("dataclasses/person: test status", "[Person]")
{
    Cell cell = Cell(0);
    cell.microcells().push_back(Microcell(0));
    cell.microcells()[0].people().push_back(0);
    cell.people().push_back(Person(0,0,0));
    Person& subject = cell.people()[0];
    REQUIRE(subject.status() == InfectionStatus::Susceptible);
    subject.setStatus(InfectionStatus::Dead);
    REQUIRE(subject.status() == InfectionStatus::Dead);
    subject.setStatus(InfectionStatus::Susceptible);
    REQUIRE(subject.status() == InfectionStatus::Susceptible);
    
    auto test = [&](InfectionStatus status)
    {
        subject.updateStatus(&cell, status, 0);
        REQUIRE(subject.status() == status);
    };
    test(InfectionStatus::Susceptible);
    test(InfectionStatus::Dead);
    test(InfectionStatus::Exposed);
    test(InfectionStatus::InfectGP);
    test(InfectionStatus::Recovered);
}

TEST_CASE("dataclasses/person: test setHousehold", "[Person]")
{
    Person subject = Person(0,0,0);
    size_t hh = static_cast<size_t>((std::rand() % 500) * 2);
    REQUIRE(subject.setHousehold(hh));
    REQUIRE(subject.setHousehold(
        static_cast<size_t>((std::rand()%500) * 2 + 1)) == false);
    REQUIRE(subject.household() == hh);
}

TEST_CASE("dataclasses/person: test places", "[Person]")
{
    Person subject = Person(0, 0, 0);
    for (size_t i = 0; i < 5; i++) subject.places().insert(std::make_pair(i, std::rand()));
    REQUIRE(subject.places().size() == 5);
}

TEST_CASE("dataclasses/person: test forEachPlace", "[Person]")
{
    Person subject = Person(0, 0, 0);
    Population population = Population();
    population.cells().push_back(std::make_shared<Cell>(0));
    population.cells()[0]->people().push_back(subject);
    for (size_t i = 0; i < 5; i++)
    {
        population.places().push_back(Place(i));
        subject.addPlace(population, population.cells()[0].get(), i, 0);
    }
    REQUIRE(subject.places().size() == 5);

    auto callback = [&](Place* place, size_t)
    {
        REQUIRE(place->isMember(0, 0));
    };
    REQUIRE_NOTHROW(subject.forEachPlace(population, callback));
}

TEST_CASE("dataclasses/person: test removePlace", "[Person]")
{
    Population population = Population();
    population.cells().push_back(std::make_shared<Cell>(0));
    population.cells()[0]->people().emplace_back(0,0,0);
    Person& subject = population.cells()[0]->people()[0];

    for (size_t i = 0; i < 5; i++)
    {
        population.places().emplace_back(i);
    }
    std::map<size_t, std::set<size_t>> _places;
    for (size_t i = 0; i < 5; i++)
    {
        for (size_t j = 0; j < 10; j++)
        {
            size_t r = static_cast<size_t>(std::rand()%10);
            subject.addPlace(population, population.cells()[0].get(),
                i, r);
            _places[i].insert(r);
        }
    }

    size_t ctr = 0;
    for (const auto& p : _places) ctr += p.second.size();
    REQUIRE(subject.places().size() == ctr);

    for (size_t i = 0; i < 10; i++)
    {
        size_t p = static_cast<size_t>(std::rand()%5);
        size_t g = static_cast<size_t>(std::rand()%15);
        subject.removePlace(population, population.cells()[0].get(), p, g);
        _places[p].erase(g);
    }

    ctr = 0;
    for (const auto& p : _places) ctr += p.second.size();
    REQUIRE(subject.places().size() == ctr);

    for (size_t p = 0; p < 5; p++)
    {
        _places[p].clear();
        subject.removePlaceAllGroups(population, population.cells()[0].get(), p);
    }
    REQUIRE(subject.places().empty());
}
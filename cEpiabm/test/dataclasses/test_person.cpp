#include "dataclasses/person.hpp"

#include "../catch/catch.hpp"

using namespace epiabm;

TEST_CASE("dataclasses/person: test initialize person", "[Person]")
{
    Person subject = Person(5, 10);
    REQUIRE(subject.cellPos() == 5);
    REQUIRE(subject.microcellPos() == 10);
    REQUIRE_NOTHROW(subject.params());
    REQUIRE(subject.status() == InfectionStatus::Susceptible);
}

TEST_CASE("dataclasses/person: test status", "[Person]")
{
    Person subject = Person(0,0);
    REQUIRE(subject.status() == InfectionStatus::Susceptible);
    
    auto test = [&](InfectionStatus status)
    {
        subject.setStatus(status);
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
    Person subject = Person(0,0);
    size_t hh = static_cast<size_t>((std::rand() % 500) * 2);
    REQUIRE(subject.setHousehold(hh));
    REQUIRE(subject.setHousehold(
        static_cast<size_t>((std::rand()%500) * 2 + 1)) == false);
    REQUIRE(subject.household() == hh);
}

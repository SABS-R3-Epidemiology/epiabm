#include "dataclasses/person.hpp"

#include <catch2/catch_test_macros.hpp>

using namespace epiabm;

TEST_CASE("person: test initialize person", "[Person]")
{
    Person subject = Person(5, 10);
    REQUIRE(subject.cellPos() == 5);
    REQUIRE(subject.microcellPos() == 10);
    REQUIRE_NOTHROW(subject.params());
    REQUIRE(subject.status() == InfectionStatus::Susceptible);
}

TEST_CASE("person: test status", "[Person]")
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


#include "dataclasses/cell.hpp"

#include "../catch/catch.hpp"

#include <random>

using namespace epiabm;

inline CompartmentCounter makeSubject(size_t n_people)
{
    std::vector<Person> people = std::vector<Person>();
    people.reserve(n_people);
    for (size_t i = 0; i < n_people; i++) people.push_back(Person(0, i, i));
    CompartmentCounter subject = CompartmentCounter();
    subject.initialize(people);
    return subject;
}

TEST_CASE("dataclasses/compartment_counter: test initialize", "[CompartmentCounter]")
{
    CompartmentCounter subject = CompartmentCounter();
    REQUIRE(subject(InfectionStatus::Susceptible) == 0);
}

TEST_CASE("dataclasses/compartment_counter: test initialize compartment counting", "[CompartmentCounter]")
{
    CompartmentCounter subject = makeSubject(100);
    REQUIRE(subject(InfectionStatus::Susceptible) == 100);
    REQUIRE(subject(InfectionStatus::Exposed) == 0);
}

TEST_CASE("dataclasses/compartment_counter: test notify", "[CompartmentCounter]")
{
    CompartmentCounter subject = makeSubject(100);
    REQUIRE(subject(InfectionStatus::Susceptible) == 100);
    REQUIRE(subject(InfectionStatus::Exposed) == 0);

    size_t n_exposed = static_cast<size_t>(std::rand()) % 90 + 10;
    for (size_t i = 0; i < n_exposed; i++)
        subject.notify(InfectionStatus::Susceptible, InfectionStatus::Exposed);

    REQUIRE(subject(InfectionStatus::Susceptible) == 100 - n_exposed);
    REQUIRE(subject(InfectionStatus::Exposed) == n_exposed);
}

TEST_CASE("dataclasses/compartment_counter: test initialize cell", "[CompartmentCounter]")
{
    Cell cell = Cell(0);
    for (size_t i = 0; i < 100; i++) cell.people().push_back(Person(0, i, i));

    CompartmentCounter subject = CompartmentCounter();
    subject.initialize(&cell, {1, 2, 3, 4, 5});

    REQUIRE(subject(InfectionStatus::Susceptible) == 5);
    REQUIRE(subject(InfectionStatus::Exposed) == 0);
}

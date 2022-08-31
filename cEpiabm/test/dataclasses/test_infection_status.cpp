
#include "dataclasses/cell.hpp"

#include "../catch/catch.hpp"

#include <random>

using namespace epiabm;

TEST_CASE("dataclasses/infection_status: test status_string", "[InfectionStatus]")
{
    REQUIRE_NOTHROW(status_string(InfectionStatus::Susceptible));
    REQUIRE_NOTHROW(status_string(InfectionStatus::Exposed));
    REQUIRE_NOTHROW(status_string(InfectionStatus::InfectASympt));
    REQUIRE_NOTHROW(status_string(InfectionStatus::InfectMild));
    REQUIRE_NOTHROW(status_string(InfectionStatus::InfectGP));
    REQUIRE_NOTHROW(status_string(InfectionStatus::InfectHosp));
    REQUIRE_NOTHROW(status_string(InfectionStatus::InfectICU));
    REQUIRE_NOTHROW(status_string(InfectionStatus::InfectICURecov));
    REQUIRE_NOTHROW(status_string(InfectionStatus::Recovered));
    REQUIRE_NOTHROW(status_string(InfectionStatus::Dead));
    REQUIRE_NOTHROW(status_string(static_cast<InfectionStatus>(20)));
}

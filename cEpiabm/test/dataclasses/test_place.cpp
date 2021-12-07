
#include "dataclasses/place.hpp"

#include <catch2/catch_test_macros.hpp>

#include <random>

using namespace epiabm;
TEST_CASE("dataclasses/place: test initialize place", "[Place]")
{
    Place subject = Place(5);
    REQUIRE(subject.microcellPos() == 5);
}

TEST_CASE("dataclasses/place: test destructor", "[Place]")
{
    {
        MembersInterface* mi = new Place(5);
        Place* subject = dynamic_cast<Place*>(mi);
        REQUIRE(subject->microcellPos() == 5);
        delete mi;
        mi = nullptr;
        subject = nullptr;
    }
}

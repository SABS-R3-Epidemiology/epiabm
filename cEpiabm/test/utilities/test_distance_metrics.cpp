#include "utility/distance_metrics.hpp"

#include "../catch/catch.hpp"

using namespace epiabm;

TEST_CASE("utility/distance_metrics: test distance metric init", "[DistanceMetrics]")
{   // tests the Dist function returns the same as the DistEuclid
    DistanceMetrics subject = DistanceMetrics()
}

TEST_CASE("utility/distance_metrics: test distance metric", "[DistanceMetrics]")
{   // tests the Dist function returns the same as the DistEuclid
    auto loc = std::make_pair(1.0, 1.0);
    double subject = DistanceMetrics::Dist(loc, loc);
    double euclid = DistanceMetrics::DistEuclid(loc, loc);
    REQUIRE(subject == euclid);

    auto loc2 = std::make_pair(1.0, 0.0);
    subject = DistanceMetrics::Dist(loc, loc2);
    euclid = DistanceMetrics::DistEuclid(loc, loc2);
    REQUIRE(subject == euclid);
}

TEST_CASE("utility/distance_metrics: test Euclidean distance metric", "[DistanceMetrics]")
{   
    auto loc = std::make_pair(1.0, 1.0);
    auto loc2 = std::make_pair(0.0, 1.0);
    double subject = DistanceMetrics::DistEuclid(loc, loc);
    REQUIRE(subject == 0);
    subject = DistanceMetrics::DistEuclid(loc, loc2);
    REQUIRE(subject == 1.0);
    loc2.first = -1.0;
    subject = DistanceMetrics::DistEuclid(loc, loc2);
    REQUIRE(subject == 2.0);
}

TEST_CASE("utility/distance_metrics: test Covidsim distance metric", "[DistanceMetrics]")
{   //these are all curretnly 2 which is helpful
    auto loc = std::make_pair(1.0, 1.0);
    auto loc2 = loc;
    loc2.first = 0.0;
    double subject = DistanceMetrics::DistCovidsim(loc, loc);
    REQUIRE(subject == 2);
    subject = DistanceMetrics::DistCovidsim(loc, loc2);
    REQUIRE(subject == 2);
    loc2.second = -1.0;
    subject = DistanceMetrics::DistCovidsim(loc, loc2);
    REQUIRE(subject == 2);
}

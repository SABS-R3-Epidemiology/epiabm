

#include "utilities/inverse_cdf.hpp"

#include "../catch/catch.hpp"

#include <random>

using namespace epiabm;

TEST_CASE("utilities/inverse_cdf: test initialize inverse cdf", "[InverseCDF]")
{
    InverseCDF subject = InverseCDF();
    REQUIRE(subject.mean() == 0);
    InverseCDF subject2(1.0);
    REQUIRE(subject2.mean() == 1.0);
}

TEST_CASE("utilities/inverse_cdf: test setNegLog", "[InverseCDF]")
{
    InverseCDF subject = InverseCDF();
    REQUIRE_NOTHROW(subject.setNegLog(1.0));
}

TEST_CASE("utilities/inverse_cdf: test assignExponent", "[InverseCDF]")
{
    InverseCDF subject = InverseCDF();
    REQUIRE_NOTHROW(subject.assignExponent());
    REQUIRE_NOTHROW(subject.assignExponent(1.0));
}


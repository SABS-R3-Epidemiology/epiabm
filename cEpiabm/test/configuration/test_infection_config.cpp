
#include "configuration/infection_config.hpp"
#include "configuration/json.hpp"
#include "logfile.hpp"

#include "helpers.hpp"
#include "../catch/catch.hpp"

#include <random>
#include <fstream>

using namespace epiabm;

TEST_CASE("infection_config: test constructor", "[InfectionConfig]")
{
    InfectionConfigPtr subject = std::make_shared<InfectionConfig>();
    REQUIRE(subject->hostProgressionConfig != nullptr);

    checkParameter(subject->basicReproductionNum, 10);
    checkParameter(subject->infectionRadius, 10);
    checkParameter(subject->probSymptomatic, 10);
    checkParameter(subject->symptInfectiousness, 10);
    checkParameter(subject->asymptInfectiousness, 10);
    checkParameter(subject->latentToSymptDelay, 10);

    checkParameter(subject->falsePositiveRate, 10);

    checkParameter(subject->householdTransmission, 10);
    checkParameter(subject->placeTransmission, 10);
}

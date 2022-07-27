
#include "configuration/simulation_config.hpp"
#include "configuration/json.hpp"
#include "logfile.hpp"

#include "helpers.hpp"
#include "../catch/catch.hpp"

#include <random>
#include <fstream>

using namespace epiabm;

TEST_CASE("simulation_config: test constructor", "[SimulationConfig]")
{
    SimulationConfigPtr subject = std::make_shared<SimulationConfig>();
    REQUIRE(subject->infectionConfig != nullptr);
    REQUIRE(subject->populationConfig != nullptr);

    checkParameter(subject->timestepsPerDay);
}

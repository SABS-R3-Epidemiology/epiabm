
#include "configuration/population_config.hpp"
#include "configuration/json.hpp"
#include "logfile.hpp"

#include "helpers.hpp"
#include "../catch/catch.hpp"

#include <random>
#include <fstream>

using namespace epiabm;

TEST_CASE("population_config: test constructor", "[PopulationConfig]")
{
    PopulationConfigPtr subject = std::make_shared<PopulationConfig>();

    checkParameter(subject->age_contacts, 10);
    checkParameter(subject->age_proportions, 10);
}


#include "configuration/host_progression_config.hpp"
#include "configuration/json.hpp"
#include "logfile.hpp"

#include "helpers.hpp"
#include "../catch/catch.hpp"

#include <random>
#include <fstream>

using namespace epiabm;

TEST_CASE("host_progression_config: test constructor", "[HostProgressionConfig]")
{
    HostProgressionConfigPtr subject = std::make_shared<HostProgressionConfig>();

    checkParameter(subject->latentPeriodICDF, 10);
    checkParameter(subject->asymptToRecovICDF, 10);
    checkParameter(subject->mildToRecovICDF, 10);
    checkParameter(subject->gpToRecovICDF, 10);
    checkParameter(subject->gpToHospICDF, 10);
    checkParameter(subject->gpToDeathICDF, 10);
    checkParameter(subject->hospToRecovICDF, 10);
    checkParameter(subject->hospToICUICDF, 10);
    checkParameter(subject->hospToDeathICDF, 10);
    checkParameter(subject->icuToICURecovICDF, 10);
    checkParameter(subject->icuToDeathICDF, 10);
    checkParameter(subject->icuRecovToRecovICDF, 10);

    checkParameter(subject->use_ages, 10);
    checkParameter(subject->prob_gp_to_hosp, 10);
    checkParameter(subject->prob_gp_to_recov, 10);
    checkParameter(subject->prob_exposed_to_asympt, 10);
    checkParameter(subject->prob_exposed_to_gp, 10);
    checkParameter(subject->prob_exposed_to_mild, 10);
    checkParameter(subject->prob_hosp_to_death, 10);
    checkParameter(subject->prob_hosp_to_recov, 10);
    checkParameter(subject->prob_hosp_to_icu, 10);
    checkParameter(subject->prob_icu_to_death, 10);
    checkParameter(subject->prob_icu_to_icurecov, 10);

    REQUIRE(subject->infectiousness_profile.size() == 0);
}

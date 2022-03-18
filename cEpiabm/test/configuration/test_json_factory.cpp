
#include "configuration/simulation_config.hpp"
#include "configuration/json_factory.hpp"
#include "configuration/json.hpp"
#include "logfile.hpp"

#include "../catch/catch.hpp"

#include <random>
#include <fstream>

using namespace epiabm;

inline const json::json getConfig()
{
    std::ifstream ifs("../testdata/test_config.json");
    json::json j;
    ifs >> j;
    return j;
}

TEST_CASE("json_factory: test loadConfig", "[JsonFactory]")
{
    ConfigurationFactoryPtr f = std::make_shared<JsonFactory>();
    CHECK_NOTHROW(f->loadConfig("../testdata/test_config.json"));
}

TEST_CASE("json_factory: test errors", "[JsonFactory]")
{
    JsonFactoryPtr f = std::make_shared<JsonFactory>();
    LogFile::Instance()->configure(0, "output/test_json_factory.log");
    
    {
        json::json j = getConfig();
        j["infection_config"]["host_progression_config"].erase("mean_hosp_to_icu");
        REQUIRE_THROWS(f->loadConfig(j));
    }
    
    {
        json::json j = getConfig();
        j["infection_config"]["host_progression_config"].erase("asympt_infect_icdf");
        REQUIRE_THROWS(f->loadConfig(j));
    }
    
    {
        json::json j = getConfig();
        j["infection_config"].erase("host_progression_config");
        REQUIRE_THROWS(f->loadConfig(j));
    }

    {
        json::json j = getConfig();
        j["infection_config"].erase("infection_radius");
        REQUIRE_THROWS(f->loadConfig(j));
    }
    
    {
        json::json j = getConfig();
        j.erase("infection_config");
        REQUIRE_THROWS(f->loadConfig(j));
    }

    {
        json::json j = getConfig();
        j.erase("timesteps_per_day");
        REQUIRE_NOTHROW(f->loadConfig(j));
    }
}

TEST_CASE("json_factory: test constructor", "[JsonFactory]")
{
    {
        ConfigurationFactoryInterface* i = new JsonFactory();
        [[maybe_unused]] JsonFactory* subject = dynamic_cast<JsonFactory*>(i);
        delete i;
        i = nullptr;
        subject = nullptr;
    }
    {
        [[maybe_unused]] ConfigurationFactoryInterface* i = new ConfigurationFactoryInterface();
        delete i;
        i = nullptr;
    }
}

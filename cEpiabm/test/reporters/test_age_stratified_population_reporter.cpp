
#include "population_factory.hpp"
#include "household_linker.hpp"
#include "reporters/age_stratified_population_reporter.hpp"

#include "../catch/catch.hpp"

#include <random>

using namespace epiabm;

TEST_CASE("reporters/age_stratified_population_reporter: test initialize", "[AgeStratifiedPopulationReporter]")
{
    PopulationPtr population = PopulationFactory().makePopulation(10, 10, 1000);
    population->cells()[0]->people()[0].setStatus(InfectionStatus::InfectASympt);
    HouseholdLinker().linkHouseholds(population, 1, 100, std::optional<size_t>());
    population->initialize();

    AgeStratifiedPopulationReporter subject = AgeStratifiedPopulationReporter("test_output/test_population_compartment_reporter.csv");
    REQUIRE_NOTHROW(subject.setup(population));
    REQUIRE_NOTHROW(subject.compartments());
    REQUIRE_NOTHROW(subject.report(population, 0));
    REQUIRE_NOTHROW(subject.teardown());
}

TEST_CASE("reporters/age_stratified_population_reporter: test destructor", "[AgeStratifiedPopulationReporter]")
{
    {
        TimestepReporterInterface* i = new AgeStratifiedPopulationReporter("test_output/test_destructor.csv");
        [[maybe_unused]] AgeStratifiedPopulationReporter* subject = dynamic_cast<AgeStratifiedPopulationReporter*>(i);
        delete i;
        i = nullptr;
        subject = nullptr;
    }
}

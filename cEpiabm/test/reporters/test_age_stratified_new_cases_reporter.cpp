
#include "population_factory.hpp"
#include "household_linker.hpp"
#include "reporters/age_stratified_new_cases_reporter.hpp"

#include "../catch/catch.hpp"

#include <random>

using namespace epiabm;

TEST_CASE("reporters/age_stratified_new_cases_reporter: test initialize", "[AgeStratifiedNewCasesReporter]")
{
    PopulationPtr population = PopulationFactory().makePopulation(10, 10, 1000);
    population->cells()[0]->people()[0].setStatus(InfectionStatus::InfectASympt);
    HouseholdLinker().linkHouseholds(population, 1, 100, std::optional<size_t>());
    population->initialize();

    AgeStratifiedNewCasesReporter subject = AgeStratifiedNewCasesReporter("test_output/test_population_compartment_reporter.csv");
    REQUIRE_NOTHROW(subject.setup(population));
    REQUIRE_NOTHROW(subject.report(population, 0));
    REQUIRE_NOTHROW(subject.teardown());
}

TEST_CASE("reporters/age_stratified_new_cases_reporter: test destructor", "[AgeStratifiedNewCasesReporter]")
{
    {
        TimestepReporterInterface* i = new AgeStratifiedNewCasesReporter("test_output/test_destructor.csv");
        [[maybe_unused]] AgeStratifiedNewCasesReporter* subject = dynamic_cast<AgeStratifiedNewCasesReporter*>(i);
        delete i;
        i = nullptr;
        subject = nullptr;
    }
}

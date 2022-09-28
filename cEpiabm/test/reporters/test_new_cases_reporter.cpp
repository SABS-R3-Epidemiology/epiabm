
#include "population_factory.hpp"
#include "household_linker.hpp"
#include "reporters/new_cases_reporter.hpp"

#include "../catch/catch.hpp"

#include <random>

using namespace epiabm;

TEST_CASE("reporters/new_cases_reporter: test initialize", "[NewCasesReporter]")
{
    PopulationPtr population = PopulationFactory().makePopulation(10, 10, 1000);
    population->cells()[0]->people()[0].setStatus(InfectionStatus::InfectASympt);
    HouseholdLinker().linkHouseholds(population, 1, 100, std::optional<size_t>());
    population->initialize();

    NewCasesReporter subject = NewCasesReporter("test_output/test_population_compartment_reporter.csv");
    REQUIRE_NOTHROW(subject.setup(population));
    REQUIRE_NOTHROW(subject.report(population, 0));
    REQUIRE_NOTHROW(subject.teardown());
}

TEST_CASE("reporters/new_cases_reporter: test destructor", "[NewCasesReporter]")
{
    {
        TimestepReporterInterface* i = new NewCasesReporter("test_output/test_destructor.csv");
        [[maybe_unused]] NewCasesReporter* subject = dynamic_cast<NewCasesReporter*>(i);
        delete i;
        i = nullptr;
        subject = nullptr;
    }
}

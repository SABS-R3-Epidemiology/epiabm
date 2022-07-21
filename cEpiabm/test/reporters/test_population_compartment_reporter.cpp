
#include "population_factory.hpp"
#include "household_linker.hpp"
#include "reporters/population_compartment_reporter.hpp"

#include "../catch/catch.hpp"

#include <random>

using namespace epiabm;

TEST_CASE("reporters/population_compartment_reporter: test initialize", "[PopulationCompartmentReporter]")
{
    PopulationPtr population = PopulationFactory().makePopulation(10, 10, 1000);
    HouseholdLinker().linkHouseholds(population, 1, 100);
    population->initialize();

    PopulationCompartmentReporter subject = PopulationCompartmentReporter("test_output/test_population_compartment_reporter.csv");
    REQUIRE_NOTHROW(subject.setup(population));
    REQUIRE_NOTHROW(subject.compartments());
    REQUIRE_NOTHROW(subject.report(population, 0));
    REQUIRE_NOTHROW(subject.teardown());
}

TEST_CASE("reporters/population_compartment_reporter: test destructor", "[PopulationCompartmentReporter]")
{
    {
        TimestepReporterInterface* i = new PopulationCompartmentReporter("test_output/test_destructor.csv");
        [[maybe_unused]] PopulationCompartmentReporter* subject = dynamic_cast<PopulationCompartmentReporter*>(i);
        delete i;
        i = nullptr;
        subject = nullptr;
    }
}

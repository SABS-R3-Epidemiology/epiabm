
#include "population_factory.hpp"
#include "household_linker.hpp"
#include "reporters/percell_compartment_reporter.hpp"

#include "../catch/catch.hpp"

#include <random>

using namespace epiabm;

TEST_CASE("reporters/percell_compartment_reporter: test initialize", "[PerCellCompartmentReporter]")
{
    PopulationPtr population = PopulationFactory().makePopulation(10, 10, 1000);
    HouseholdLinker().linkHouseholds(population, 1, 100, std::optional<size_t>());
    population->initialize();

    PerCellCompartmentReporter subject = PerCellCompartmentReporter("test_output");
    REQUIRE_NOTHROW(subject.setup(population));
    REQUIRE_NOTHROW(subject.compartments());
    REQUIRE_NOTHROW(subject.report(population, 0));
    REQUIRE_NOTHROW(subject.teardown());
}

TEST_CASE("reporters/percell_compartment_reporter: test destructor", "[PerCellCompartmentReporter]")
{
    {
        TimestepReporterInterface* i = new PerCellCompartmentReporter("test_output");
        [[maybe_unused]] PerCellCompartmentReporter* subject = dynamic_cast<PerCellCompartmentReporter*>(i);
        delete i;
        i = nullptr;
        subject = nullptr;
    }
}

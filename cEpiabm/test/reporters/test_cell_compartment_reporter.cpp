
#include "population_factory.hpp"
#include "household_linker.hpp"
#include "reporters/cell_compartment_reporter.hpp"
#include "logfile.hpp"

#include "../catch/catch.hpp"

#include <random>

using namespace epiabm;

TEST_CASE("reporters/cell_compartment_reporter: test initialize", "[CellCompartmentReporter]")
{
    PopulationPtr population = PopulationFactory().makePopulation(10, 10, 1000);
    HouseholdLinker().linkHouseholds(population, 1, 100, std::optional<size_t>());
    population->initialize();

    CellCompartmentReporter subject = CellCompartmentReporter("test_output");
    REQUIRE_NOTHROW(subject.setup(population));
    REQUIRE_NOTHROW(subject.compartments());
    REQUIRE_NOTHROW(subject.report(population, 0));
    REQUIRE_NOTHROW(subject.teardown());
}

TEST_CASE("reporters/cell_compartment_reporter: test destructor", "[CellCompartmentReporter]")
{
    {
        TimestepReporterInterface* i = new CellCompartmentReporter("test_output");
        [[maybe_unused]] CellCompartmentReporter* subject = dynamic_cast<CellCompartmentReporter*>(i);
        delete i;
        i = nullptr;
        subject = nullptr;
    }
    {
        TimestepReporterInterface* i = new TimestepReporterInterface(
            std::filesystem::path("test_output/test.csv"));
        i->report(PopulationPtr(), 0);
        delete i;
        i = nullptr;
    }
    {
        std::string tmp = "test_output/test.csv";
        [[maybe_unused]] TimestepReporterInterface* i = new TimestepReporterInterface(tmp);
        delete i;
        i = nullptr;
    }
}

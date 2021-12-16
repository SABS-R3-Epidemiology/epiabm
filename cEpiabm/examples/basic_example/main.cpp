
#include "logfile.hpp"

#include "population_factory.hpp"
#include "household_linker.hpp"
#include "simulations/basic_simulation.hpp"
#include "sweeps/household_sweep.hpp"
#include "sweeps/new_infection_sweep.hpp"
#include "sweeps/basic_host_progression_sweep.hpp"
#include "sweeps/random_seed_sweep.hpp"
#include "reporters/cell_compartment_reporter.hpp"
#include "reporters/percell_compartment_reporter.hpp"
#include "reporters/population_compartment_reporter.hpp"

#include <random>

void run()
{
    using namespace epiabm;

    std::srand(100);

    LogFile::Instance()->configure(2, std::filesystem::path("output/log.log"));

    PopulationPtr population = PopulationFactory().makePopulation(10, 10, 1000);
    HouseholdLinker().linkHouseholds(population, 5, 100);
    population->initialize();

    {
        RandomSeedSweep randomizer = RandomSeedSweep(200);
        randomizer.bind_population(population);
        randomizer(0);
    }

    BasicSimulation simulation = BasicSimulation(population);

    simulation.addSweep(std::make_shared<HouseholdSweep>());
    simulation.addSweep(std::make_shared<NewInfectionSweep>());
    simulation.addSweep(std::make_shared<BasicHostProgressionSweep>());

    simulation.addTimestepReporter(
        std::make_shared<CellCompartmentReporter>("output/results_pertimestep"));
    simulation.addTimestepReporter(
        std::make_shared<PerCellCompartmentReporter>("output/results_percell"));
    simulation.addTimestepReporter(
        std::make_shared<PopulationCompartmentReporter>("output/population_results.csv"));

    simulation.simulate(100);
}


int main()
{
    try
    {
        run();
    }
    catch (std::exception& e)
    {
        std::cout << "Exception: " << e.what();
    }
    catch (...)
    {
        std::cout << "Unknown Exception" << std::endl;
    }
}


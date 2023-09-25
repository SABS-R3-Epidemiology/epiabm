
#include "logfile.hpp"

#include "population_factory.hpp"
#include "toy_population_factory.hpp"
#include "household_linker.hpp"
#include "simulations/basic_simulation.hpp"
#include "simulations/threaded_simulation.hpp"
#include "sweeps/household_sweep.hpp"
#include "sweeps/new_infection_sweep.hpp"
#include "sweeps/spatial_sweep.hpp"
#include "sweeps/basic_host_progression_sweep.hpp"
#include "sweeps/host_progression_sweep.hpp"
#include "sweeps/random_seed_sweep.hpp"
#include "configuration/json_factory.hpp"
#include "reporters/cell_compartment_reporter.hpp"
#include "reporters/percell_compartment_reporter.hpp"
#include "reporters/population_compartment_reporter.hpp"

#include <random>

void run()
{
    using namespace epiabm;

    std::srand(100); // random seed

    // Setup Logfile
    LogFile::Instance()->configure(2, std::filesystem::path("output/log.log"));

    SimulationConfigPtr cfg = JsonFactory().loadConfig(std::filesystem::path("parameters.json"));

    // Make Population and Link Households
    PopulationPtr population = ToyPopulationFactory().makePopulation(100000, 10, 100, 50, 0, 2);
    //PopulationPtr population = PopulationFactory().makePopulation(200, 1, 25);
    //HouseholdLinker().linkHouseholds(population, 2, 100);
    population->initialize();

    std::cout << "Initialized Population" << std::endl;

    // Randomly Seed Population with Infections
    {
        RandomSeedSweep randomizer = RandomSeedSweep(cfg, 10000);
        randomizer.bind_population(population);
        randomizer(0);
    }

    // Create Simulation
    ThreadedSimulation simulation = ThreadedSimulation(population, std::optional<size_t>());

    // Add Sweeps
    simulation.addSweep(std::make_shared<HouseholdSweep>(cfg), 0);
    simulation.addSweep(std::make_shared<SpatialSweep>(cfg), 1);
    simulation.addSweep(std::make_shared<NewInfectionSweep>(cfg), 2);
    simulation.addSweep(std::make_shared<HostProgressionSweep>(cfg), 3);

    // Set which reporters to use
    simulation.addTimestepReporter(
        std::make_shared<PopulationCompartmentReporter>("output/population_results.csv"));
    simulation.addTimestepReporter(
        std::make_shared<CellCompartmentReporter>("output/results_pertimestep"));
    simulation.addTimestepReporter(
        std::make_shared<PerCellCompartmentReporter>("output/results_percell"));

    std::cout << "Beginning Simulation" << std::endl;
    simulation.simulate(100); // Run Simulation for 100 steps
}


int main()
{
    //try
    //{
        run();
    /*}
    catch (std::exception& e)
    {
        std::cout << "Exception: " << e.what();
    }
    catch (...)
    {
        std::cout << "Unknown Exception" << std::endl;
    }*/
}



#include "population_factory.hpp"

#include <chrono>
#include <iostream>
#include <random>

int main()
{
    int n_cells, n_microcells, n_people;
    std::cin >> n_cells >> n_microcells >> n_people;

    std::cout << "Starting" << std::endl;

    auto t0 = std::chrono::steady_clock::now();

    epiabm::PopulationPtr population;
    
    {
        epiabm::PopulationFactory factory = epiabm::PopulationFactory();
        population = factory.makePopulation();
        factory.addCells(population, n_cells);
        for (auto cell : population->cells())
        {
            factory.addMicrocells(cell, n_microcells);
            for (auto mcell : cell->microcells())
            {
                factory.addPeople(mcell, n_people);
            }
        }
    }

    auto t1 = std::chrono::steady_clock::now();
    std::cout << "Initialized in " << std::chrono::duration_cast<std::chrono::milliseconds>(t1 - t0).count() << "ms" << std::endl;

    long long int ctr = 0;
    for (auto cell : population->cells())
    {
        for (auto mcell : cell->microcells())
        {
            for (auto p1 : mcell->people())
            {
                for (auto p2 : mcell->people())
                {
                    ctr += 1;
                }
            }
        }
    }

    auto t2 = std::chrono::steady_clock::now();
    std::cout << "Finished: " << ctr << std::endl;
    std::cout << "Double for loop took " << std::chrono::duration_cast<std::chrono::seconds>(t2 - t1).count() << "s" << std::endl;


    return 0;
}

#ifndef _EPIABM_BENCHMARK_TESTS_HPP
#define _EPIABM_BENCHMARK_TESTS_HPP

#include "population_factory.hpp"

#include <iostream>


namespace epiabm
{

    long long int nestedTest(PopulationPtr population)
    {
        long long int ctr = 0;
        for (auto cell : population->cells())
        {
            for (auto mcell : cell->microcells())
            {
                for (auto p1 : mcell->people())
                {
                    for (auto p2: mcell->people())
                    {
                        ctr += 1;
                    }
                }
            }
        }

        std::cout << ctr << std::endl;

        return ctr;
    }

} // namespace epiabm

#endif // _EPIABM_BENCHMARK_TESTS_HPP

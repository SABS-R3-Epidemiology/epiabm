#include "toy_population_factory.hpp"
#include "population_factory.hpp"

#include <random>
#include <functional>
#include <algorithm>
#include <iterator>
#include <vector>

namespace epiabm
{
    inline std::vector<size_t> generate_multinomial(size_t nGroups, size_t nRolls)
    {
        std::vector<double> probabilities = std::vector<double>(nGroups, 1.0);
        std::vector<size_t> multinomial = std::vector<size_t>(nGroups, 0);

        std::random_device rd;
        std::mt19937 gen(rd());
        std::discrete_distribution<size_t> distribution =
            std::discrete_distribution<size_t>(probabilities.begin(), probabilities.end());
        for (size_t i = 0; i < nRolls; i++) multinomial[distribution(gen)]++;
        return multinomial;
        //return std::vector<size_t>(nGroups, nRolls/nGroups);
    }

    inline void distributePeople(PopulationPtr population, size_t nCells, size_t nMicrocells, size_t nPeople)
    {
        std::vector<size_t> multinomial = generate_multinomial(nCells*nMicrocells, nPeople);

        for (size_t ci = 0; ci < nCells; ci++)
        {
            Cell* cell = &population->cells()[ci];
            
            size_t nPeopleInCell = static_cast<size_t>(std::accumulate(
                std::next(multinomial.begin(), static_cast<long>(ci*nMicrocells)),
                std::next(multinomial.begin(), static_cast<long>((ci+1)*nMicrocells)), 0));
            cell->people().reserve(nPeopleInCell);

            for (size_t mci = 0; mci < nMicrocells; mci++)
            {
                Microcell* microcell = &cell->microcells()[mci];
                microcell->people().reserve(multinomial[ci*nMicrocells + mci]);

                for (size_t pi = 0; pi < multinomial[ci*nMicrocells + mci]; pi++)
                {
                    cell->people().emplace_back(mci, cell->people().size(), pi);
                    microcell->people().push_back(cell->people().size()-1);
                }
            }
        }
    }

    inline void addHouseholds(PopulationPtr population, size_t nHouseholdsPerMicrocell)
    {
        for (size_t ci = 0; ci < population->cells().size(); ci++)
        {
            Cell* cell = &population->cells()[ci];
            for (size_t mi = 0; mi < cell->microcells().size(); mi++)
            {
                Microcell* microcell = &cell->microcells()[mi];
                microcell->households().reserve(nHouseholdsPerMicrocell);
                std::vector<size_t> distrib = generate_multinomial(
                    nHouseholdsPerMicrocell, microcell->people().size());
                size_t pi = 0;
                for (size_t hi = 0; hi < nHouseholdsPerMicrocell; hi++)
                {
                    microcell->households().push_back(std::make_shared<Household>(hi));
                    for (size_t i = 0; i < distrib[hi]; i++)
                    {
                        microcell->households()[hi]->addMember(pi);
                        microcell->getPerson(*cell, pi).setHousehold(hi);
                        pi++;
                    }
                }
            }
        }
    }

    PopulationPtr ToyPopulationFactory::makePopulation(
        size_t populationSize, size_t nCells, size_t nMicrocellsPerCell,
        size_t nHouseholds, size_t)
    {
        PopulationFactory factory = PopulationFactory();
        PopulationPtr population = factory.makePopulation(nCells, nMicrocellsPerCell, 0);

        distributePeople(population, nCells, nMicrocellsPerCell, populationSize);
        if (nHouseholds > 0) addHouseholds(population, nHouseholds);

        return population;
    }

}

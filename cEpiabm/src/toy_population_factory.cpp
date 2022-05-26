#include "toy_population_factory.hpp"
#include "population_factory.hpp"

#include <random>
#include <functional>
#include <algorithm>
#include <iterator>
#include <vector>

namespace epiabm
{
    inline std::vector<size_t> generate_multinomial(
        size_t nGroups, size_t nRolls, std::optional<size_t> seed)
    {
        std::vector<double> probabilities = std::vector<double>(nGroups, 1.0);
        std::vector<size_t> multinomial = std::vector<size_t>(nGroups, 0);

        if (!seed.has_value())
        {
            std::random_device rd;
            seed = rd();
        }
        std::mt19937 gen(seed.value());
        std::discrete_distribution<size_t> distribution =
            std::discrete_distribution<size_t>(probabilities.begin(), probabilities.end());
        for (size_t i = 0; i < nRolls; i++) multinomial[distribution(gen)]++;
        return multinomial;
        //return std::vector<size_t>(nGroups, nRolls/nGroups);
    }

    inline void distributePeople(PopulationPtr population, size_t nCells, size_t nMicrocells, size_t nPeople, size_t seed)
    {
        std::vector<size_t> multinomial = generate_multinomial(nCells*nMicrocells, nPeople, seed);

        for (size_t ci = 0; ci < nCells; ci++)
        {
            Cell* cell = population->cells()[ci].get();
            
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

    inline void addHouseholds(PopulationPtr population, size_t nHouseholdsPerMicrocell, size_t seed)
    {
        for (size_t ci = 0; ci < population->cells().size(); ci++)
        {
            Cell* cell = population->cells()[ci].get();
            for (size_t mi = 0; mi < cell->microcells().size(); mi++)
            {
                Microcell* microcell = &cell->microcells()[mi];
                microcell->households().reserve(nHouseholdsPerMicrocell);
                std::vector<size_t> distrib = generate_multinomial(
                    nHouseholdsPerMicrocell, microcell->people().size(), seed);
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

    inline void assignCellLocations(PopulationPtr population)
    {
        size_t nCells = population->cells().size();
        size_t gridLength = static_cast<size_t>(ceil(sqrt(static_cast<double>(nCells))));
        for (size_t ci = 0; ci < nCells; ci++)
        {
            Cell& cell = *population->cells()[ci];
            double cx = static_cast<double>(ci%gridLength)/static_cast<double>(gridLength);
            double cy = static_cast<double>(ci/gridLength)/static_cast<double>(gridLength);
            cell.setLocation(
                std::make_pair(cx, cy));
        }
    }

    PopulationPtr ToyPopulationFactory::makePopulation(
        size_t populationSize, size_t nCells, size_t nMicrocellsPerCell,
        size_t nHouseholds, size_t, std::optional<size_t> seed)
    {
        PopulationFactory factory = PopulationFactory();
        PopulationPtr population = factory.makePopulation(nCells, nMicrocellsPerCell, 0);

        distributePeople(population, nCells, nMicrocellsPerCell, populationSize, seed.value_or(0));
        if (nHouseholds > 0) addHouseholds(population, nHouseholds, seed.value_or(0) + 1);

        assignCellLocations(population);

        return population;
    }

}

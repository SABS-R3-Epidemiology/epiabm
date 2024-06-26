
#include "population_factory.hpp"

namespace epiabm
{

    PopulationPtr PopulationFactory::makePopulation()
    {
        return std::make_shared<Population>();
    }

    PopulationPtr PopulationFactory::makePopulation(
        size_t n_cells,
        size_t n_microcells,
        size_t n_people)
    {
        PopulationPtr population = makePopulation();
        population->cells().reserve(n_cells);
        addCells(population, n_cells);
        for (size_t i = 0; i < n_cells; i++)
        {
            population->cells()[i]->people().reserve(n_microcells * n_people);
            population->cells()[i]->microcells().reserve(n_microcells);
            addMicrocells(population->cells()[i].get(), n_microcells);
            for (size_t j = 0; j < n_microcells; j++)
            {
                population->cells()[i]->microcells()[j].people().reserve(n_people);
                addPeople(
                    population->cells()[i].get(),
                    j,
                    n_people);
            }
        }
        return population;
    }

    void PopulationFactory::addCell(PopulationPtr population)
    {
        population->cells().push_back(
            std::make_shared<Cell>(population->cells().size()));
    }

    void PopulationFactory::addCells(PopulationPtr population, size_t n)
    {
        //population->cells().reserve(population->cells().size() + n);
        for (size_t i = 0; i < n; i++)
        {
            addCell(population);
        }
    }

    void PopulationFactory::addMicrocell(Cell* cell)
    {
        cell->microcells().emplace_back(cell->microcells().size());
    }

    void PopulationFactory::addMicrocells(Cell* cell, size_t n)
    {
        //cell->microcells().reserve(cell->microcells().size() + n);
        for (size_t i = 0; i < n; i++)
        {
            addMicrocell(cell);
        }
    }

    void PopulationFactory::addPerson(Cell* cell, size_t microcell_index)
    {
        cell->people().emplace_back(
            microcell_index, cell->people().size(), cell->getMicrocell(microcell_index).people().size());
        cell->getMicrocell(microcell_index).people().push_back(
            cell->people().size()-1);
    }

    void PopulationFactory::addPeople(Cell* cell, size_t microcell_index, size_t n)
    {
        //cell->people().reserve(cell->people().size() + n);
        //microcell->people().reserve(microcell->people().size() + n);
        for (size_t i = 0; i < n; i++)
        {
            addPerson(cell, microcell_index);
        }
    }

    void PopulationFactory::addHousehold(Microcell* microcell)
    {
        size_t i = microcell->households().size();
        microcell->households().push_back(
            std::make_shared<Household>(i));
    }
    void PopulationFactory::addHouseholds(Microcell* microcell, size_t n)
    {
        for (size_t i = 0; i < n; i++)
            addHousehold(microcell);
    }

    void PopulationFactory::addPlace(PopulationPtr population)
    {
        size_t i = population->places().size();
        population->places().emplace_back(i);
    }
    void PopulationFactory::addPlaces(PopulationPtr population, size_t n)
    {
        for (size_t i = 0; i < n; i++)
            addPlace(population);
    }

} // namespace epiabm

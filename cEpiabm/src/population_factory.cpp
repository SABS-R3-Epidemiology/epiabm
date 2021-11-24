
#include "population_factory.hpp"

namespace epiabm
{

    PopulationPtr PopulationFactory::makePopulation()
    {
        return std::make_shared<Population>();
    }

    void PopulationFactory::addCell(PopulationPtr population)
    {
        population->cells().push_back(std::make_shared<Cell>());
    }

    void PopulationFactory::addCells(PopulationPtr population, int n)
    {
        for (int i = 0; i < n; i++)
        {
            addCell(population);
        }
    }

    void PopulationFactory::addMicrocell(CellPtr cell)
    {
        cell->microcells().push_back(std::make_shared<Microcell>(
            cell, cell->microcells().size()));
    }

    void PopulationFactory::addMicrocells(CellPtr cell, int n)
    {
        for (int i = 0; i < n; i++)
        {
            addMicrocell(cell);
        }
    }

    void PopulationFactory::addPerson(MicrocellPtr microcell)
    {
        PersonPtr newPerson = std::make_shared<Person>(
            microcell, microcell->cell()->people().size());
        microcell->cell()->people().push_back(newPerson);
        microcell->people().push_back(newPerson);
    }

    void PopulationFactory::addPeople(MicrocellPtr microcell, int n)
    {
        for (int i = 0; i < n; i++)
        {
            addPerson(microcell);
        }
    }

} // namespace epiabm

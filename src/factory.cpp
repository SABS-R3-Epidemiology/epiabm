
#include "factory.hpp"

namespace seir
{

    PopulationPtr Factory::makePopulation()
    {
        return std::make_shared<Population>();
    }

    void Factory::addCell(PopulationPtr population)
    {
        population->m_cells.push_back(std::make_shared<Cell>());
    }

    void Factory::addCells(PopulationPtr population, int n)
    {
        for (int i = 0; i < n; i++)
        {
            addCell(population);
        }
    }

    void Factory::addMicrocell(CellPtr cell)
    {
        cell->m_microcells.push_back(std::make_shared<Microcell>(cell));
    }

    void Factory::addMicrocells(CellPtr cell, int n)
    {
        for (int i = 0; i < n; i++)
        {
            addMicrocell(cell);
        }
    }

    void Factory::addPerson(MicrocellPtr microcell)
    {
        PersonPtr newPerson = std::make_shared<Person>(microcell);
        microcell->cell()->m_people.push_back(newPerson);
        microcell->m_people.push_back(newPerson);
    }

    void Factory::addPeople(MicrocellPtr microcell, int n)
    {
        for (int i = 0; i < n; i++)
        {
            addPerson(microcell);
        }
    }

} // namespace seir

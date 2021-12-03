#ifndef EPIABM_POPULATION_FACTORY_HPP
#define EPIABM_POPULATION_FACTORY_HPP

#include "dataclasses/population.hpp"
#include "dataclasses/cell.hpp"
#include "dataclasses/microcell.hpp"
#include "dataclasses/place.hpp"
#include "dataclasses/person.hpp"

#include <iostream>

namespace epiabm
{

    class PopulationFactory
    {
    private:
    public:
        PopulationPtr makePopulation();
        PopulationPtr makePopulation(size_t n_cells, size_t n_microcells, size_t n_people);
    
        void addCell(PopulationPtr population);
        void addMicrocell(Cell* cell);
        void addPerson(Cell* cell, Microcell* microcell);

        void addCells(PopulationPtr population, size_t n);
        void addMicrocells(Cell* cell, size_t n);
        void addPeople(Cell* cell, Microcell* microcell, size_t n);

        void print() { std::cout << "Hello World!" << std::endl; }
        
    private:
    };

} // namespace epiabm

#endif // EPIABM_POPULATION_FACTORY_HPP

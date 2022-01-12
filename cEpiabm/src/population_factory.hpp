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
        PopulationPtr makePopulation(
            size_t n_cells, 
            size_t n_microcells,
            size_t n_people);
    
        void addCell(PopulationPtr population);
        void addMicrocell(Cell* cell);
        void addPerson(Cell* cell, size_t microcell_index);

        void addCells(PopulationPtr population, size_t n);
        void addMicrocells(Cell* cell, size_t n);
        void addPeople(Cell* cell, size_t microcell_index, size_t n);
        
    private:
    };

} // namespace epiabm

#endif // EPIABM_POPULATION_FACTORY_HPP

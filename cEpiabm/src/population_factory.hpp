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

        /**
         * @brief Create a Basic Population
         * 
         * Create a Population with n_cells, n_microcells :class:`Microcell` in each cell, and n_people :class:`People` in each microcell.
         * 
         * @param n_cells 
         * @param n_microcells 
         * @param n_people 
         * @return PopulationPtr 
         */
        PopulationPtr makePopulation(
            size_t n_cells, // n cells in population
            size_t n_microcells, // n microcels per cell
            size_t n_people); // n people per microcell
    
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

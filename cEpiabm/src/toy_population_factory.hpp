#ifndef EPIABM_TOY_POPULATION_FACTORY_HPP
#define EPIABM_TOY_POPULATION_FACTORY_HPP

#include "dataclasses/population.hpp"
#include "dataclasses/cell.hpp"
#include "dataclasses/microcell.hpp"
#include "dataclasses/place.hpp"
#include "dataclasses/person.hpp"


namespace epiabm
{

    class ToyPopulationFactory
    {
        private:
        public:
            PopulationPtr makePopulation(
                size_t populationSize, size_t nCells, size_t nMicrocells,
                size_t nHouseholds, size_t nPlaces, std::optional<size_t> seed);

        private:
    };

}


#endif // EPIABM_TOY_POPULATION_FACTORY_HPP
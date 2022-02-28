#ifndef EPIABM_DATACLASSES_POPULATION_HPP
#define EPIABM_DATACLASSES_POPULATION_HPP

#include "cell.hpp"
#include "place.hpp"

#include <functional>
#include <vector>
#include <memory>

namespace epiabm
{
    
    class Population
    {
    private:
        std::vector<Cell> m_cells;
        std::vector<Place> m_places;
        
    public:
        Population();
        ~Population() = default;
        
        /**
         * @brief Callback each Cell in Population.
         * callback function is applied to each cell.
         * stops if callback function returns false.
         * @param callback 
         */
        void forEachCell(std::function<bool(Cell*)> callback);
        void forEachPlace(std::function<bool(Place*)> callback);

        std::vector<Cell>& cells();
        std::vector<Place>& places();

        /**
         * @brief Pre-simulation start initialization
         * Called by simulation class post initialization to setup any helper structures
         */
        void initialize();

    private:
    };

    typedef std::shared_ptr<Population> PopulationPtr;

} // namespace epiabm

#endif // EPIABM_DATACLASSES_POPULATION_HPP

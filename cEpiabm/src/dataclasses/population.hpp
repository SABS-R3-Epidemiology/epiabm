#ifndef EPIABM_DATACLASSES_POPULATION_HPP
#define EPIABM_DATACLASSES_POPULATION_HPP

#include "cell.hpp"
#include "place.hpp"

#include <functional>
#include <vector>
#include <memory>

namespace epiabm
{
    const size_t N_AGE_GROUPS = 17; // Each age group is 5 years

    /**
     * @brief Class representing a population
     * 
     */
    class Population
    {
    private:
        std::vector<CellPtr> m_cells;
        std::vector<Place> m_places;
        
    public:
        Population();
        ~Population();
        
        void forEachCell(std::function<bool(Cell*)> callback);
        void forEachPlace(std::function<bool(Place*)> callback);

        std::vector<CellPtr>& cells();
        std::vector<Place>& places();

        void initialize();

    private:
    };

    typedef std::shared_ptr<Population> PopulationPtr;

} // namespace epiabm

#endif // EPIABM_DATACLASSES_POPULATION_HPP

#ifndef EPIABM_DATACLASSES_POPULATION_HPP
#define EPIABM_DATACLASSES_POPULATION_HPP

#include "cell.hpp"

#include <functional>
#include <vector>
#include <memory>

namespace epiabm
{
    
    class Population
    {
    private:
        std::vector<Cell> m_cells;
        
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

        /**
         * @brief Get Cells in Population.
         * 
         * @return std::vector<Cell>& 
         */
        std::vector<Cell>& cells();
    
    private:
    };

    typedef std::shared_ptr<Population> PopulationPtr;

} // namespace epiabm

#endif // EPIABM_DATACLASSES_POPULATION_HPP

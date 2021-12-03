#ifndef _EPIABM_DATACLASSES_POPULATION_HPP
#define _EPIABM_DATACLASSES_POPULATION_HPP

#include "cell.hpp"

#include <functional>
#include <vector>
#include <memory>
#include <iostream>

namespace epiabm
{
    
    class Population
    {
    private:
        std::vector<Cell> m_cells;
        
    public:
        Population();
        ~Population() = default;

        void forEachCell(std::function<bool(Cell*)>& callback);
        std::vector<Cell>& cells() { return m_cells; }

        void print()
        {
            std::cout << "Population with " << m_cells.size() << " Cells!" << std::endl;
        }
    
    private:
        friend class Factory;
    };

    typedef std::shared_ptr<Population> PopulationPtr;
    
} // namespace epiabm

#endif // _EPIABM_DATACLASSES_POPULATION_HPP

#ifndef _EPIABM_DATACLASSES_POPULATION_HPP
#define _EPIABM_DATACLASSES_POPULATION_HPP

#include "types.hpp"

#include <functional>
#include <vector>
#include <memory>
#include <iostream>

namespace epiabm
{

    class Population
    {
    private:
        std::vector<CellPtr> m_cells;
        
    public:
        Population();
        ~Population() = default;

        void forEachCell(std::function<bool(CellPtr)>& callback);
        std::vector<CellPtr>& cells() { return m_cells; }

        void print()
        {
            std::cout << "Population with " << m_cells.size() << " Cells!" << std::endl;
        }
    
    private:
        friend class Factory;
    };
    
} // namespace epiabm

#endif // _EPIABM_DATACLASSES_POPULATION_HPP

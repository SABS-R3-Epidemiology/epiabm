#ifndef _COVIDSIM_DATACLASSES_POPULATION_HPP
#define _COVIDSIM_DATACLASSES_POPULATION_HPP

#include "types.hpp"

#include <boost/python.hpp>
#include <boost/function.hpp>

#include <functional>
#include <vector>
#include <memory>
#include <iostream>

namespace seir
{

    class Population
    {
    private:
        std::vector<CellPtr> m_cells;
    public:
        Population();

        void forEachCell(boost::function<bool(CellPtr)> callback);

        Cell* getCell(int i) { return m_cells[i].get(); }

        void print() { std::cout << "Population with " << m_cells.size() << " Cells!" << std::endl; }
    private:
        friend class Factory;
    };
    
} // namespace seir

#endif // _COVIDSIM_DATACLASSES_POPULATION_HPP

#include "population.hpp"

namespace epiabm
{

    Population::Population() :
        m_cells(0)
    {}

    void Population::forEachCell(std::function<bool(CellPtr)>& callback)
    {
        for (size_t i = 0; i < m_cells.size(); i++)
        {
            callback(m_cells[i]);
        }
    }

} // namespace epiabm

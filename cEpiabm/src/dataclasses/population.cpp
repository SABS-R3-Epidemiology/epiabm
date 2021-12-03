#include "population.hpp"

namespace epiabm
{

    Population::Population() :
        m_cells()
    {}

    void Population::forEachCell(std::function<bool(Cell*)> callback)
    {
        for (size_t i = 0; i < m_cells.size(); i++)
        {
            if (!callback(&m_cells[i])) return;
        }
    }

} // namespace epiabm

#include "population.hpp"

namespace seir
{

    Population::Population() :
        m_cells(0)
    {}

    void Population::forEachCell(boost::function<bool(CellPtr)> callback)
    {
        for (size_t i = 0; i < m_cells.size(); i++)
        {
            callback(m_cells[i]);
        }
    }

} // namespace seir
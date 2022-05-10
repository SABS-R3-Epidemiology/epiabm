#include "population.hpp"

#include <iostream>

namespace epiabm
{

    Population::Population() :
        m_cells()
    {
        std::cout << "Created Population" << std::endl;
    }

    Population::~Population()
    {
        std::cout << "Deleted Population" << std::endl;
    }

    void Population::forEachCell(std::function<bool(Cell*)> callback)
    {
        for (size_t i = 0; i < m_cells.size(); i++)
        {
            if (!callback(&m_cells[i])) return;
        }
    }

    void Population::forEachPlace(std::function<bool(Place*)> callback)
    {
        for (size_t i = 0; i < m_places.size(); i++)
            if (!callback(&m_places[i])) return;
    }

    std::vector<Cell>& Population::cells() { return m_cells; }

    std::vector<Place>& Population::places() { return m_places; }

    void Population::initialize()
    {
        for (size_t i = 0; i < m_cells.size(); i++)
        {
            m_cells[i].initialize();
        }
    }

} // namespace epiabm

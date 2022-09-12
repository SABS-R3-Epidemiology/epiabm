#include "population.hpp"

#include <iostream>

namespace epiabm
{

    /**
     * @brief Construct a new Population:: Population object
     * 
     */
    Population::Population() :
        m_cells()
    {
        std::cout << "Created Population" << std::endl;
    }

    /**
     * @brief Destroy the Population:: Population object
     * 
     */
    Population::~Population()
    {
        std::cout << "Deleted Population" << std::endl;
    }

    /**
     * @brief Callback each Cell in Population.
     * callback function is applied to each cell.
     * stops if callback function returns false.
     * @param callback Callback to apply to each cell
     */
    void Population::forEachCell(std::function<bool(Cell*)> callback)
    {
        for (size_t i = 0; i < m_cells.size(); i++)
        {
            if (!callback(m_cells[i].get())) return;
        }
    }

    /**
     * @brief Callback each Place in Population
     * 
     * Callback function is applied to each place
     * Terminates early if callback function returns false
     * 
     * @param callback Callback to apply to each place
     */
    void Population::forEachPlace(std::function<bool(Place*)> callback)
    {
        for (size_t i = 0; i < m_places.size(); i++)
            if (!callback(&m_places[i])) return;
    }

    /**
     * @brief Get reference to population's cells vector
     * 
     * @return std::vector<CellPtr>& Reference to population's cells vector
     */
    std::vector<CellPtr>& Population::cells() { return m_cells; }

    /**
     * @brief Get reference to population's places vector
     * 
     * @return std::vector<Place>& Reference to population's places vector
     */
    std::vector<Place>& Population::places() { return m_places; }

    /**
     * @brief Pre-simulation start initialization
     * Called by simulation class post initialization to setup any helper structures
     */
    void Population::initialize()
    {
        for (size_t i = 0; i < m_cells.size(); i++)
        {
            m_cells[i]->initialize();
        }
    }

} // namespace epiabm

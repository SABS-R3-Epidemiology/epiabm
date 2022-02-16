
#include "spatial_sweep.hpp"
#include "../covidsim.hpp"
#include "../dataclasses/cell.hpp"

#include <functional>
#include <random>
#include <iterator>
#include <algorithm>

namespace epiabm
{

    SpatialSweep::SpatialSweep() {}

    void SpatialSweep::operator()(const unsigned short timestep)
    {
        if (m_population->cells().size() <= 1){
            return;  // no intercell infections if only one cell
        }
        m_population->forEachCell(
            std::bind(&SpatialSweep::cellCallback, this, timestep, std::placeholders::_1));
    }

    inline std::vector<Cell*> getCellsToInfect(std::vector<Cell>& cells, Cell* currentCell, size_t n)
    {
        std::vector<size_t> allCells = std::vector<size_t>();
        allCells.reserve(n-1);
        for (size_t i = 0; i < n; i++)
            if (i != currentCell->index()) allCells.push_back(i);

        std::vector<Cell*> chosenCells = std::vector<Cell*>();
        std::sample(allCells.begin(), allCells.end(),
            [&](size_t i) { chosenCells.push_back(&cells[i]); }, n,
            std::mt19937{std::random_device{}()});
        return chosenCells;
    }

    /**
     * @brief Cell callback
     * Determine number of infections
     * @param timestep
     * @param cell
     * @return true
     * @return false
     */
    bool SpatialSweep::cellCallback(const unsigned short timestep, Cell* cell)
    {
        if (cell->numInfectious() <= 0){
            return true;  // Break out as there are no infectors in cell
        }
        double ave_num_of_infections = Covidsim::CalcCellInf(cell, timestep);

        std::default_random_engine generator;
        std::poisson_distribution<int> distribution(ave_num_of_infections);
        int number_to_infect = distribution(generator);
        
        std::vector<Cell*> inf_cells = getCellsToInfect(m_population->cells(), cell, number_to_infect);

        Person* infector;
        cell->sampleInfectious(1, [&](Person* p) { infector = p; return true; });

        for (Cell* inf_cell_addr : inf_cells){
            if (inf_cell_addr->people().size() < 1) continue;

            size_t infectee_index = static_cast<size_t>(std::rand())%inf_cell_addr->people().size();
            Person* infectee = &inf_cell_addr->people()[infectee_index];

            // Could put the lines below in a callback like household_sweep?
            if (infectee->status() != InfectionStatus::Susceptible){
                continue;
            }

            double infectiousness = Covidsim::CalcSpaceInf(cell, infector, timestep);
            double susceptibility = Covidsim::CalcSpaceSusc(cell, infectee, timestep);
            double foi = infectiousness * susceptibility;

            if ((static_cast<double>(std::rand() % 1000000) / static_cast<double>(1000000)) < foi)
            {
                // Infection attempt is successful
                cell->enqueuePerson(infectee->cellPos());
            }
        }
        return true;
    }

} // namespace epiabm


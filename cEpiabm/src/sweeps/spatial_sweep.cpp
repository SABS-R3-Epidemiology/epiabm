
#include "spatial_sweep.hpp"
#include "../covidsim.hpp"
#include "../dataclasses/cell.hpp"  // again seem to be having problems with relative path
#include "../utility/distance_metrics.hpp"
#include "../reporters/cell_compartment_reporter.hpp"

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
        std::vector<double> weightVector = getWeightsFromCells(cells, currentCell);
        std::vector<size_t> chosenCellIndices = std::vector<size_t>();
        std::random_device rd;
        std::mt19937 generator(rd());
        std::discrete_distribution<Cell*> distribution(weightVector.begin(), weightVector.end()); 

        for(int i=0; i<n; ++i){
            int cell_ind = distribution(generator); // generator spits out integers
            chosenCellIndices.push_back(cell_ind);
        }

        std::vector<Cell*> chosen = std::vector<Cell*>();
        chosen.reserve(n);
        for (const auto i : chosenCellIndices) chosen.push_back(&cells[i]);
        return chosen;
    }

    inline std::vector<double> getWeightsFromCells(std::vector<Cell>& cells, Cell* currentCell,
    bool doDistance = true, bool doCovidsim = false)
    {
        std::vector<double> weightVector;
        if (doDistance){
            std::pair <double, double> current_loc = currentCell->getLocation();
            for (Cell& cell : cells){
                weightVector.push_back(DistanceMetrics::dist(cell.getLocation(), current_loc));
            }
        }
        else if (doCovidsim)
        {
            for (Cell& cell : cells){
                if (&cell == currentCell){ // want to compare pointers here
                    weightVector.push_back(0);
                }
                else {
                    size_t num_infectious = cell.numInfectious();
                    weightVector.push_back(static_cast<int>(num_infectious));
                }
            }
        }
        return weightVector;
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
        size_t number_to_infect = static_cast<size_t>(distribution(generator));
        
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


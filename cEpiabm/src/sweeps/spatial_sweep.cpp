
#include "spatial_sweep.hpp"
#include "../covidsim.hpp"
#include "../dataclasses/cell.hpp"
#include "../logfile.hpp"

#include <functional>
#include <random>
#include <iterator>
#include <algorithm>

namespace epiabm
{
    SpatialSweep::SpatialSweep() {}

    SpatialSweep::SpatialSweep(SimulationConfigPtr cfg) :
        SweepInterface(cfg)
    {
    }

    void SpatialSweep::operator()(const unsigned short timestep)
    {
        LOG << LOG_LEVEL_DEBUG << "Beginning Spatial Sweep " << timestep;
        if (m_population->cells().size() <= 1){
            return;  // no intercell infections if only one cell
        }
        m_population->forEachCell(
            std::bind(&SpatialSweep::cellCallback, this, timestep, std::placeholders::_1));
        LOG << LOG_LEVEL_DEBUG << "Finished Spatial Sweep " << timestep;
    }

    inline std::vector<Cell*> SpatialSweep::getCellsToInfect(std::vector<Cell>& cells, Cell* currentCell, size_t n)
    {
        std::vector<size_t> allCells = std::vector<size_t>();
        allCells.reserve(cells.size()-1);
        for (size_t i = 0; i < cells.size(); i++)
            if (i != currentCell->index()) allCells.push_back(i);

        std::vector<size_t> chosenCellIndices = std::vector<size_t>();
        std::sample(allCells.begin(), allCells.end(),
            std::back_inserter(chosenCellIndices), n,
            m_cfg->randomManager->g().generator());
        
        std::vector<Cell*> chosen = std::vector<Cell*>();
        chosen.reserve(n);
        for (const auto i : chosenCellIndices) chosen.push_back(&cells[i]);
        return chosen;
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
        double ave_num_of_infections = calcCellInf(cell, timestep);

        std::default_random_engine generator;
        std::poisson_distribution<int> distribution(ave_num_of_infections);
        size_t number_to_infect = static_cast<size_t>(distribution(m_cfg->randomManager->g().generator()));
        
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

            double infectiousness = calcSpaceInf(cell, infector, timestep);
            double susceptibility = calcSpaceSusc(cell, infectee, timestep);
            double foi = infectiousness * susceptibility;

            if (m_cfg->randomManager->g().randf<double>() < foi)
            {
                // Infection attempt is successful
                LOG << LOG_LEVEL_INFO << "Spatial infection between ("
                    << cell->index() << "," << infector->cellPos() << ") and ("
                    << inf_cell_addr->index() << "," << infectee->cellPos() << ")";
                inf_cell_addr->enqueuePerson(infectee->cellPos());
            }
        }
        return true;
    }

    double SpatialSweep::calcCellInf(
        Cell* cell,
        unsigned short int )
    {
        return m_cfg->infectionConfig->basicReproductionNum * static_cast<double>(cell->numInfectious());
    }

    double SpatialSweep::calcSpaceInf(
        Cell* /*cell*/,
        Person* /*infector*/,
        unsigned short int )
    {
        return 0.5;
    }

    double SpatialSweep::calcSpaceSusc(
        Cell* /*cell*/,
        Person* /*infectee*/,
        unsigned short int )
    {
        return 0.2;
    }

} // namespace epiabm


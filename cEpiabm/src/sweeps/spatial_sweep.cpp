
#include "spatial_sweep.hpp"
#include "../covidsim.hpp"
#include "../dataclasses/cell.hpp" // again seem to be having problems with relative path
#include "../utilities/distance_metrics.hpp"
#include "../reporters/cell_compartment_reporter.hpp"
#include "../logfile.hpp"

#include <functional>
#include <random>
#include <iterator>
#include <algorithm>

namespace epiabm
{
    SpatialSweep::SpatialSweep() {}

    SpatialSweep::SpatialSweep(SimulationConfigPtr cfg) :
        SweepInterface(cfg),
        m_counter(0)
    {
    }

    void SpatialSweep::operator()(const unsigned short timestep)
    {
        LOG << LOG_LEVEL_DEBUG << "Beginning Spatial Sweep " << timestep;
        m_counter = 0;
        if (m_population->cells().size() <= 1){
            return;  // no intercell infections if only one cell
        }
        m_population->forEachCell(
            std::bind(&SpatialSweep::cellCallback, this, timestep, std::placeholders::_1));
        LOG << LOG_LEVEL_INFO << "Spatial Sweep " << timestep << " caused " << m_counter << " new infections.";
        LOG << LOG_LEVEL_DEBUG << "Finished Spatial Sweep " << timestep;
    }

    inline std::vector<double> SpatialSweep::getWeightsFromCells(std::vector<Cell> &cells, Cell *currentCell,
                                                   bool doDistance = true, bool doCovidsim = false)
    {
        std::vector<double> weightVector;
        if (doDistance)
        {
            std::pair<double, double> current_loc = currentCell->location();
            for (Cell &cell : cells)
            {
                double dist = DistanceMetrics::Dist(cell.location(), current_loc);
                weightVector.push_back(
                    dist < m_cfg->infectionConfig->infectionRadius ?
                        1.0/dist : 0);
            }
        }
        else if (doCovidsim)
        {
            for (Cell &cell : cells)
            {
                if (&cell == currentCell)
                { // want to compare pointers here
                    weightVector.push_back(0);
                }
                else
                {
                    size_t num_infectious = cell.numInfectious();
                    weightVector.push_back(static_cast<int>(num_infectious));
                }
            }
        }
        return weightVector;
    }

    inline std::vector<size_t> SpatialSweep::getCellsToInfect(std::vector<Cell> &cells, Cell *currentCell, size_t n)
    {
        std::vector<double> weightVector = getWeightsFromCells(cells, currentCell);
        std::vector<size_t> chosenCellIndices = std::vector<size_t>();
        std::discrete_distribution<size_t> distribution(weightVector.begin(), weightVector.end());

        for (size_t i = 0; i < n; ++i)
        {
            size_t cell_ind = distribution(m_cfg->randomManager->g().generator()); // generator spits out integers
            chosenCellIndices.push_back(cell_ind);
        }
        return chosenCellIndices;
    }

    /**
     * @brief Cell callback
     * Determine number of infections
     * @param timestep
     * @param cell
     * @return true
     * @return false
     */
    bool SpatialSweep::cellCallback(const unsigned short timestep, Cell *cell)
    {
        if (cell->numInfectious() <= 0)
        {
            return true; // Break out as there are no infectors in cell
        }
        double ave_num_of_infections = calcCellInf(cell, timestep);

        std::poisson_distribution<int> distribution(ave_num_of_infections);
        size_t number_to_infect = static_cast<size_t>(distribution(m_cfg->randomManager->g().generator()));
        LOG << LOG_LEVEL_DEBUG << "Cell " << cell->index() << " distributing " << number_to_infect << " spatial infections.";

        std::vector<size_t> inf_cell_indices = getCellsToInfect(m_population->cells(), cell, number_to_infect);

        Person *infector;
        cell->sampleInfectious(1, [&](Person *p)
                               { infector = p; return true; });

        for (const size_t infCellIndex : inf_cell_indices)
        {
            Cell* inf_cell_addr = &m_population->cells()[infCellIndex];
            if (inf_cell_addr->people().size() < 1)
                continue;

            size_t infectee_index = static_cast<size_t>(m_cfg->randomManager->g().randi(RAND_MAX)) % inf_cell_addr->people().size();
            Person *infectee = &inf_cell_addr->people()[infectee_index];

            // Could put the lines below in a callback like household_sweep?
            if (infectee->status() != InfectionStatus::Susceptible)
            {
                continue;
            }

            double infectiousness = calcSpaceInf(cell, infector, timestep);
            double susceptibility = calcSpaceSusc(cell, infectee, timestep);
            double foi = infectiousness * susceptibility;

            if (m_cfg->randomManager->g().randf<double>() < foi)
            {
                // Infection attempt is successful
                LOG << LOG_LEVEL_DEBUG << "Spatial infection between ("
                    << cell->index() << "," << infector->cellPos() << ") and ("
                    << inf_cell_addr->index() << "," << infectee->cellPos() << ")";
                m_counter++;
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
        Person* infector,
        unsigned short int )
    {
        return m_cfg->infectionConfig->hostProgressionConfig->use_ages ?
            static_cast<double>(infector->params().infectiousness) * m_cfg->populationConfig->age_contacts[infector->params().age_group]:
            static_cast<double>(infector->params().infectiousness);
    }

    double SpatialSweep::calcSpaceSusc(
        Cell* /*cell*/,
        Person* infectee,
        unsigned short int )
    {
        return m_cfg->infectionConfig->hostProgressionConfig->use_ages ?
            m_cfg->populationConfig->age_contacts[infectee->params().age_group]:
            1.0;
    }

} // namespace epiabm

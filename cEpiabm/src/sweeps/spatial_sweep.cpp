
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

        std::vector<Cell*> pos_inf_cells;  // List of pointers to cells to infect
        for (Cell any_cell : m_population->cells()){
            pos_inf_cells.push_back(&any_cell);
        }
        pos_inf_cells.erase(std::remove_if(
            pos_inf_cells.begin(), pos_inf_cells.end(), 
            [&](Cell* other) { return other == cell; }), pos_inf_cells.end());  // Remove current cell from list

        // std::vector<size_t> cell_list_indices;
        // std::random_device rd;  // Obtain a seed for the random number engine
        // std::mt19937 gen(rd()); // Standard mersenne_twister_engine seeded with rd()
        // std::uniform_int_distribution<> distrib(0, pos_inf_cells.size());  // Generate random cell index
        // for (int n = 0; n < number_to_infect; n++){
        //     cell_list_indices.push_back(distrib(gen));
        // }

        std::vector<Cell*> inf_cells = std::vector<Cell*>();
        std::sample(pos_inf_cells.begin(), pos_inf_cells.end(),
            std::back_inserter(inf_cells), number_to_infect,
            std::mt19937{std::random_device{}()});

        std::vector<Person*> possible_infectors = std::vector<Person*>();
        cell->forEachInfectious([&](Person* p) { possible_infectors.push_back(p); return true; });

        Person* infector;
        {
            std::vector<Person*> infectors = std::vector<Person*>();
            std::sample(possible_infectors.begin(), possible_infectors.end(),
                std::back_inserter(infectors), 1, std::mt19937{std::random_device{}()});
            infector = infectors[0];
        }

        for (Cell* inf_cell_addr : pos_inf_cells){
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
        //return true; // Not meant to be here?
        }
        return true;
        
    }

} // namespace epiabm


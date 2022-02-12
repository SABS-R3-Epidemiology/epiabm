
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
        pos_inf_cells.erase(std::remove(pos_inf_cells.begin(), pos_inf_cells.end(), &cell), 
                            pos_inf_cells.end());  // Remove current cell from list

        // std::vector<size_t> cell_list_indices;
        // std::random_device rd;  // Obtain a seed for the random number engine
        // std::mt19937 gen(rd()); // Standard mersenne_twister_engine seeded with rd()
        // std::uniform_int_distribution<> distrib(0, pos_inf_cells.size());  // Generate random cell index
        // for (int n = 0; n < number_to_infect; n++){
        //     cell_list_indices.push_back(distrib(gen));
        // }

        std::vector<Cell*> inf_cells = std::sample(pos_inf_cells.begin(), 
                                                   pos_inf_cells.end(),
                                                   number_to_infect, 
                                                   std::mt19937{std::random_device{}()});


        std::vector<Person> possible_infectors = (*cell).m_infectiousPeople();

        Person infector = std::sample(possible_infectors.begin(), possible_infectors.end(),
                               1, std::mt19937{std::random_device{}()});

        for (Cell* inf_cell_addr : pos_inf_cells){
            Person infectee = std::sample(inf_cell_addr->m_people.begin(), 
                                          inf_cell_addr->m_people.end(),
                                          1, 
                                          std::mt19937{std::random_device{}()});

            // Could put the lines below in a callback like household_sweep?
            if (infectee.status() != InfectionStatus::Susceptible){
                continue;
            }

            double infectiousness = Covidsim::CalcSpaceInf(cell, &infector, timestep);
            double susceptibility = Covidsim::CalcSpaceSusc(cell, &infectee, timestep);
            double foi = infectiousness * susceptibility;

            if (static_cast<double>(std::rand() % 1000000) / static_cast<double>(1000000) < foi)
            {
                // Infection attempt is successful
                cell->enqueuePerson(infectee.cellPos());
            }
        return true;
        }


    }

} // namespace epiabm


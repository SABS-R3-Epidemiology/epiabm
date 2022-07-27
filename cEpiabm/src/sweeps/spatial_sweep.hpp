#ifndef EPIABM_SWEEPS_SPATIAL_SWEEP_HPP
#define EPIABM_SWEEPS_SPATIAL_SWEEP_HPP

#include "sweep_interface.hpp"

#include <memory>
#include <random>


namespace epiabm
{

    /**
     * @brief Spread Infection between cells (spatial infection)
     * Process each infected person and try to infect all susceptibles in their household.
     * People to be newly infected get queued in their cell's people queue.
     */
    class SpatialSweep : public SweepInterface
    {
    private:
        unsigned long m_counter;

        RandomGeneratorPtr m_generator;

    public:
        SpatialSweep(SimulationConfigPtr cfg);
        ~SpatialSweep() = default;

        /**
         * @brief Perform Spatial Sweep
         * 
         * @param timestep 
         */
        void operator()(const unsigned short timestep) override;

        bool cellCallback(
            const unsigned short timestep,
            Cell* cell) override;

        bool cellInfectiousCallback(
            const unsigned short timestep,
            Cell* cell,
            Person* infectious);

    private:
        bool infectAttempt(
            const unsigned short timestep,
            Cell* cell,
            Person* infector, Person* infectee);

        inline std::vector<size_t> getCellsToInfect(
            std::vector<CellPtr>& cells, Cell* currentCell, size_t n);
        
        std::vector<double> getWeightsFromCells(std::vector<CellPtr> &cells, Cell *currentCell);

        double calcCellInf(
            Cell* cell,
            unsigned short int timestep);

        double calcSpaceInf(
            Cell* inf_cell,
            Person* infector,
            unsigned short int timestep);
        
        double calcSpaceSusc(
            Cell* cell,
            Person* infectee,
            unsigned short int timestep);
    

    }; // class SpatialSweep

    typedef std::shared_ptr<SpatialSweep> SpatialSweepPtr;


} // namespace epiabm


#endif // EPIABM_SWEEPS_SPATIAL_SWEEP_HPP
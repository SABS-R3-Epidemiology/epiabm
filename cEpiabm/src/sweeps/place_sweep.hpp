#ifndef EPIABM_SWEEPS_PLACE_SWEEP_HPP
#define EPIABM_SWEEPS_PLACE_SWEEP_HPP

#include "sweep_interface.hpp"

#include <memory>


namespace epiabm
{

    /**
     * @brief Spread Infection within Places
     * Process each infected person and try to infect all susceptibles in their place.
     * People to be newly infected get queued in their cell's people queue.
     */
    class PlaceSweep : public SweepInterface
    {
    private:
        unsigned long m_counter;

    public:
        PlaceSweep(SimulationConfigPtr cfg);
        ~PlaceSweep() = default;

        /**
         * @brief Perform Place Sweep
         * 
         * @param timestep 
         */
        void operator()(const unsigned short timestep) override;

        bool cellCallback(
            const unsigned short timestep,
            Cell* cell) override;

        bool cellInfectiousCallback(
            const unsigned short timestep,
            Cell* infectorCell, Person* infector);

    private:
        bool placeCallback(
            const unsigned short timestep,
            Cell* infectorCell, Person* infector,
            Place* place, size_t group);

        bool doInfect(
            const unsigned short timestep,
            Cell* cell, Person* infector,
            Cell* infecteeCell, Person* infectee,
            Place* place, size_t group);

        double calcPlaceInf(
            Place* place,
            Person* infector,
            const unsigned short int timestep);

        double calcPlaceFoi(
            Place* place,
            Person* infector,
            Person* infectee,
            const unsigned short int timestep);

    }; // class PlaceSweep

    typedef std::shared_ptr<PlaceSweep> PlaceSweepPtr;


} // namespace epiabm


#endif // EPIABM_SWEEPS_PLACE_SWEEP_HPP
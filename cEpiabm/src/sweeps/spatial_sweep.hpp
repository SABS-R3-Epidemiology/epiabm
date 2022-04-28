#ifndef EPIABM_SWEEPS_SPATIAL_SWEEP_HPP
#define EPIABM_SWEEPS_SPATIAL_SWEEP_HPP

#include "sweep_interface.hpp"

#include <memory>


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
    public:
        SpatialSweep();
        ~SpatialSweep() = default;

        /**
         * @brief Perform Spatial Sweep
         * 
         * @param timestep 
         */
        void operator()(const unsigned short timestep) override;

    private:
        bool cellCallback(
            const unsigned short timestep,
            Cell* cell);

        bool cellInfectiousCallback(
            const unsigned short timestep,
            Cell* cell,
            Person* infectious);

        bool infectAttempt(
            const unsigned short timestep,
            Cell* cell,
            Person* infector, Person* infectee);

    }; // class SpatialSweep

    typedef std::shared_ptr<SpatialSweep> SpatialSweepPtr;


} // namespace epiabm


#endif // EPIABM_SWEEPS_SPATIAL_SWEEP_HPP
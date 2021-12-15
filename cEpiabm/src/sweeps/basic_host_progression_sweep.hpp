#ifndef EPIABM_SWEEPS_HOST_PROGRESSION_SWEEP_HPP
#define EPIABM_SWEEPS_HOST_PROGRESSION_SWEEP_HPP

#include "sweep_interface.hpp"

#include <map>
#include <memory>
#include <stack>

namespace epiabm
{

    /**
     * @brief Replication of Covid-sim's host progression sweep without Severity
     * 
     */
    class BasicHostProgressionSweep : public SweepInterface
    {
    private:
    public:
        BasicHostProgressionSweep();
        ~BasicHostProgressionSweep() = default;

        void operator()(const unsigned short timestep) override;

    private:
        bool cellCallback(
            const unsigned short timestep,
            Cell* cell);

        bool cellExposedCallback(
            const unsigned short timestep,
            Cell* cell,
            Person* person);

        bool cellInfectiousCallback(
            const unsigned short timestep,
            Cell* cell,
            Person* person);

    private:
        unsigned short time_to_next_status(
            Person* person,
            InfectionStatus status);

        InfectionStatus first_infectious_status(
            Person* person);

        InfectionStatus next_status(
            Person* person);

    private:
    };

    typedef std::shared_ptr<BasicHostProgressionSweep> BasicHostProgressionSweepPtr;

} // namespace epiabm


#endif // EPIABM_SWEEPS_HOST_PROGRESSION_SWEEP_HPP
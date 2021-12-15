#ifndef EPIABM_SWEEPS_NEW_INFECTION_SWEEP_HPP
#define EPIABM_SWEEPS_NEW_INFECTION_SWEEP_HPP

#include "sweep_interface.hpp"
#include "../dataclasses/person.hpp"

#include <memory>


namespace epiabm
{

    class NewInfectionSweep : public SweepInterface
    {
        private:
        public:
            NewInfectionSweep();
            ~NewInfectionSweep() = default;

            void operator()(const unsigned short timestep) override;

        private:
            bool cellCallback(
                const unsigned short timestep,
                Cell* cell);

            void cellPersonQueueCallback(
                const unsigned short timestep,
                Cell* cell,
                size_t personIndex);

    }; // class NewInfectionSweep
    
    typedef std::shared_ptr<NewInfectionSweep> NewInfectionSweepPtr;

} // namespace epiabm


#endif // EPIABM_SWEEPS_NEW_INFECTION_SWEEP_HPP
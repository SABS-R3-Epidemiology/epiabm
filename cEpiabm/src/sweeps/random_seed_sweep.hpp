#ifndef EPIABM_SWEEPS_RANDOM_SEED_SWEEP_HPP
#define EPIABM_SWEEPS_RANDOM_SEED_SWEEP_HPP

#include "sweep_interface.hpp"

namespace epiabm
{
    
    class RandomSeedSweep : public SweepInterface
    {
        private:
            int m_infectRate;
            unsigned long m_infected;

        public:
            /**
             * @brief Construct a new Random Seed Sweep object
             * One in every per_n_people is updated to infectious
             * @param infection_rate 
             */
            RandomSeedSweep(SimulationConfigPtr simulationConfig, int per_n_people);
            ~RandomSeedSweep() = default;

            /**
             * @brief Sweep through population and infect people
             * 
             * @param timestep 
             */
            void operator()(const unsigned short timestep) override;

        private:
            bool cellCallback(
                const unsigned short timestep,
                Cell* cell);

            bool cellPersonCallback(
                unsigned short timestep,
                Cell* cell,
                Person* person);

        private:
    }; // class RandomSeedSweep

    typedef std::shared_ptr<RandomSeedSweep> RandomSeedSweepPtr;

} // namespace epiabm


#endif // EPIABM_SWEEPS_RANDOM_SEED_SWEEP_HPP
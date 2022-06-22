
#include "population_factory.hpp"

#include <random>

using namespace epiabm;

inline void bind_households(PopulationPtr population, size_t n_households)
{
    for (size_t c = 0; c < population->cells().size(); c++)
    {
        Cell* cell = population->cells()[c].get();
        for (size_t mc = 0; mc < cell->microcells().size(); mc++)
        {
            Microcell* microcell = &cell->microcells()[mc];
            for (size_t hh = 0; hh < n_households; hh++)
            {
                microcell->households().push_back(
                    std::make_shared<Household>(microcell->households().size()));
            }
            for (size_t p = 0; p < microcell->people().size(); p++)
            {
                if (std::rand() % 100 < 80)
                {
                    Person* person = &microcell->getPerson(*cell, p);
                    size_t hh = static_cast<size_t>(std::rand()) % n_households;
                    person->setHousehold(hh);
                    microcell->households()[hh]->addMember(p);
                }
            }
        }
    }
}

inline void random_seed(PopulationPtr population, int percentage, InfectionStatus status, unsigned short nextTime)
{
    for (size_t c = 0; c < population->cells().size(); c++)
    {
        Cell* cell = population->cells()[c].get();
        for (size_t mc = 0; mc < cell->microcells().size(); mc++)
        {
            for (size_t p = 0; p < cell->people().size(); p++)
            {
                if (std::rand() % 100 < percentage)
                {
                    Person* person = &cell->getPerson(p);
                    person->updateStatus(cell, status, 0);
                    person->params().next_status_time = nextTime;
                    person->params().infectiousness=1.0;
                }
            }
        }
    }
}
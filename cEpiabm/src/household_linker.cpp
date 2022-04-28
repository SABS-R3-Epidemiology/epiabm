
#include "household_linker.hpp"
#include "dataclasses/household.hpp"

#include <random>

namespace epiabm
{

    void HouseholdLinker::linkHouseholds(PopulationPtr population, size_t n_households, int percInHousehold, size_t seed)
    {
        std::mt19937_64 g(seed);
        population->forEachCell([&](Cell* cell)
            {
                cell->forEachMicrocell([&](Microcell* microcell)
                    {
                        // Add Households
                        for (size_t h = 0; h < n_households; h++)
                        {
                            microcell->households().push_back(
                                std::make_shared<Household>(microcell->households().size()));
                        }

                        // Assign each person to a household
                        microcell->forEachPerson(*cell, [&](Person* person)
                            {
                                if (static_cast<int>(g()) % 100 > percInHousehold) return true;
                                size_t hh = static_cast<size_t>(g()) % n_households;
                                cell->getMicrocell(person->microcell()).households()[hh]->addMember(person->microcellPos());
                                person->setHousehold(hh);
                                return true;
                            });
                        return true;
                    });
                return true;
            });
    }

} // namespace epiabm

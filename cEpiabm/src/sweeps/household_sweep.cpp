
#include "household_sweep.hpp"
#include "../covidsim.hpp"

#include <functional>
#include <random>

namespace epiabm
{

    HouseholdSweep::HouseholdSweep() {}

    void HouseholdSweep::operator()(const unsigned short timestep)
    {
        m_population->forEachCell(
            std::bind(&HouseholdSweep::cellCallback, this, timestep, std::placeholders::_1));
    }

    bool HouseholdSweep::cellCallback(const unsigned short timestep, Cell* cell)
    {
        cell->forEachInfectious(std::bind(
            &HouseholdSweep::cellInfectiousCallback, this,
            timestep, cell, std::placeholders::_1));
        return true;
    }

    bool HouseholdSweep::cellInfectiousCallback(
        const unsigned short timestep,
        Cell* cell,
        Person* infector)
    {
        // For each infectious person, Get their household then loop through potential infectees
        if (!infector->household().has_value()) return true;
        HouseholdPtr household =
            cell->getMicrocell(infector->microcell())
            .households()[infector->household().value()];
        household->forEachMember(*cell, cell->getMicrocell(infector->microcell()),
            std::bind(&HouseholdSweep::infectAttempt, this,
                timestep, cell, household, infector, std::placeholders::_1));
        return true;
    }

    bool HouseholdSweep::infectAttempt(
        const unsigned short timestep,
        Cell* cell, HouseholdPtr /*household*/,
        Person* infector, Person* infectee)
    {
        // Each interaction between an infector and infectee
        if (infectee->status() != InfectionStatus::Susceptible) return true;

        double infectiousness = Covidsim::CalcHouseInf(infector, timestep);
        double susceptibility = Covidsim::CalcHouseSusc(infector, infectee, timestep);
        double foi = infectiousness * susceptibility;

        if (static_cast<double>(std::rand()%1000000)/static_cast<double>(1000000) < foi)
        {
            // Infection attempt is successful
            cell->enqueuePerson(infectee->cellPos());
        }
        return true;
    }

} // namespace epiabm


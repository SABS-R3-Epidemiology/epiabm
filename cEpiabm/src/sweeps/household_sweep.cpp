
#include "household_sweep.hpp"
#include "../covidsim.hpp"
#include "../logfile.hpp"

#include <functional>
#include <random>

namespace epiabm
{

    HouseholdSweep::HouseholdSweep(SimulationConfigPtr cfg) :
        SweepInterface(cfg),
        m_counter(0)
    {}

    void HouseholdSweep::operator()(const unsigned short timestep)
    {
        LOG << LOG_LEVEL_DEBUG << "Beginning Household Sweep " << timestep;
        m_counter = 0;
        m_population->forEachCell(
            std::bind(&HouseholdSweep::cellCallback, this, timestep, std::placeholders::_1));
        LOG << LOG_LEVEL_INFO << "Household Sweep " << timestep << " caused " << m_counter << " new infections.";
        LOG << LOG_LEVEL_DEBUG << "Finished Household Sweep " << timestep;
    }

    /**
     * @brief Cell callback
     * Process each infectious person in the cell.
     * @param timestep
     * @param cell
     * @return true
     * @return false
     */
    bool HouseholdSweep::cellCallback(const unsigned short timestep, Cell* cell)
    {
        cell->forEachInfectious(std::bind(
            &HouseholdSweep::cellInfectiousCallback, this,
            timestep, cell, std::placeholders::_1));
        return true;
    }

    /**
     * @brief Infectious person callback
     * Process each Infectious person by finding their household and attempting to transmit to each houshold member.
     * @param timestep
     * @param cell
     * @param infector
     * @return true
     * @return false
     */
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

    /**
     * @brief Attempt to spread infection between household members
     *
     * @param timestep
     * @param cell
     * @param household
     * @param infector
     * @param infectee
     * @return true
     * @return false
    */
    bool HouseholdSweep::infectAttempt(
        const unsigned short timestep,
        Cell* cell, HouseholdPtr /*household*/,
        Person* infector, Person* infectee)
    {
        // Each interaction between an infector and infectee
        if (infectee->status() != InfectionStatus::Susceptible) return true;

        double infectiousness = calcHouseInf(infector, timestep);
        double susceptibility = calcHouseSusc(infector, infectee, timestep);
        double foi = infectiousness * susceptibility;

        if (m_cfg->randomManager->g().randf<double>() < foi)
        {
            LOG << LOG_LEVEL_DEBUG << "Household infection in cell " << cell->index()
                << " between " << infector->cellPos() << " and " << infectee->cellPos();
            // Infection attempt is successful
            cell->enqueuePerson(infectee->cellPos());
            m_counter++;
        }
        return true;
    }

    double HouseholdSweep::calcHouseInf(
        Person* infector,
        unsigned short int )
    {
        return static_cast<double>(infector->params().infectiousness) * m_cfg->infectionConfig->householdTransmission;
    }

    double HouseholdSweep::calcHouseSusc(
        Person* infector,
        Person* infectee,
        unsigned short int timestep)
    {
        return calcPersonSusc(infector, infectee, timestep);
    }

    double HouseholdSweep::calcPersonSusc(
        Person* /*infector*/,
        Person* /*infectee*/,
        unsigned short int )
    {
        return 1.0;
    }

} // namespace epiabm


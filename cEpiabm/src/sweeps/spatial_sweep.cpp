
#include "spatial_sweep.hpp"
#include "../covidsim.hpp"

#include <functional>
#include <random>

namespace epiabm
{

    SpatialSweep::SpatialSweep() {}

    void SpatialSweep::operator()(const unsigned short timestep)
    {
        m_population->forEachCell(
            std::bind(&SpatialSweep::cellCallback, this, timestep, std::placeholders::_1));
    }

    /**
     * @brief Cell callback
     * Process each infectious person in the cell.
     * @param timestep
     * @param cell
     * @return true
     * @return false
     */
    bool SpatialSweep::cellCallback(const unsigned short timestep, Cell* cell)
    {
        cell->forEachInfectious(std::bind(
            &SpatialSweep::cellInfectiousCallback, this,
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
    bool SpatialSweep::cellInfectiousCallback(
        const unsigned short timestep,
        Cell* cell,
        Person* infector)
    {
        // For each infectious person, Get their household then loop through potential infectees
        if (!infector->household().has_value()) return true;
        SpatialPtr household =
            cell->getMicrocell(infector->microcell())
            .households()[infector->household().value()];
        household->forEachMember(*cell, cell->getMicrocell(infector->microcell()),
            std::bind(&SpatialSweep::infectAttempt, this,
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
    bool SpatialSweep::infectAttempt(
        const unsigned short timestep,
        Cell* cell, SpatialPtr /*household*/,
        Person* infector, Person* infectee)
    {
        // Each interaction between an infector and infectee
        if (infectee->status() != InfectionStatus::Susceptible) return true;

        double infectiousness = Covidsim::CalcSpaceInf(cell, infector, timestep);
        double susceptibility = Covidsim::CalcSpaceSusc(cell, infectee, timestep);
        double foi = infectiousness * susceptibility;

        if (static_cast<double>(std::rand() % 1000000) / static_cast<double>(1000000) < foi)
        {
            // Infection attempt is successful
            cell->enqueuePerson(infectee->cellPos());
        }
        return true;
    }

} // namespace epiabm


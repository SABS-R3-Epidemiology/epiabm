
#include "place_sweep.hpp"
#include "../covidsim.hpp"
#include "../logfile.hpp"

#include <functional>
#include <random>

namespace epiabm
{

    PlaceSweep::PlaceSweep(SimulationConfigPtr cfg) :
        SweepInterface(cfg),
        m_counter(0)
    {}

    void PlaceSweep::operator()(const unsigned short timestep)
    {
        LOG << LOG_LEVEL_DEBUG << "Beginning Place Sweep " << timestep;
        m_counter = 0;
        m_population->forEachCell(
            std::bind(&PlaceSweep::cellCallback, this, timestep, std::placeholders::_1));
        LOG << LOG_LEVEL_INFO << "Place Sweep " << timestep << " caused " << m_counter << " new infections.";
        LOG << LOG_LEVEL_DEBUG << "Finished Place Sweep " << timestep;
    }

    /**
     * @brief Cell callback
     * Process each infectious person in the cell.
     * @param timestep
     * @param infectorCell
     * @return true
     * @return false
     */
    bool PlaceSweep::cellCallback(const unsigned short timestep, Cell* infectorCell)
    {
        infectorCell->forEachInfectious(std::bind(
            &PlaceSweep::cellInfectiousCallback, this,
            timestep, infectorCell, std::placeholders::_1));
        return true;
    }

    /**
     * @brief Infectious person callback
     * Process each Infectious person by finding their household and attempting to transmit to each houshold member.
     * @param timestep
     * @param infectorCell
     * @param infector
     * @return true
     * @return false
     */
    bool PlaceSweep::cellInfectiousCallback(
        const unsigned short timestep,
        Cell* infectorCell,
        Person* infector)
    {
        // For each infectious person, Get their place then loop through potential infectees
        infector->forEachPlace(*m_population,
            std::bind(&PlaceSweep::placeCallback, this,
                timestep, infectorCell, infector, std::placeholders::_1, std::placeholders::_2));
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
    bool PlaceSweep::placeCallback(
        const unsigned short timestep,
        Cell* infectorCell, Person* infector,
        Place* place, size_t group)
    {
        double infectiousness = calcPlaceInf(place, infector, timestep, group);

        if (infectiousness >= 1)
        {
            // LCOV_EXCL_START
            // All susceptibles should be infected if infectiousness > 1
            LOG << LOG_LEVEL_DEBUG << "Place " << place->populationPos() << " has infectiousness "
                << infectiousness << ". All susceptibel members will be infected";
            place->forEachMemberInGroup(*m_population, group,
                std::bind(&PlaceSweep::doInfect, this,
                    timestep, infectorCell, infector, 
                    std::placeholders::_1, std::placeholders::_2,
                    place, group));
            // LCOV_EXCL_STOP
        }
        else
        {
            // Binomially distribute infections
            std::binomial_distribution<size_t> distribution(
                place->membersInGroup(group).size(), infectiousness);
            size_t nInfectAttempts = distribution(m_cfg->randomManager->g().generator());

            place->sampleMembersInGroup(*m_population, group,
                nInfectAttempts,
                [&](Cell* infecteeCell, Person* infectee)
                {
                    if (infectee->status() != InfectionStatus::Susceptible) return true;

                    double foi = calcPlaceFoi(place, infector, infectee, timestep, group);
                    if (m_cfg->randomManager->g().randf<double>() < foi)
                    {
                        doInfect(timestep, infectorCell, infector,
                            infecteeCell, infectee,
                            place, group);
                    }
                    return true;
                },
                m_cfg->randomManager->g().generator());
        }
        return true;
    }

    bool PlaceSweep::doInfect(
        const unsigned short /*timestep*/,
        Cell* infectorCell, Person* infector,
        Cell* infecteeCell, Person* infectee,
        Place* place, size_t group)
    {
        if (infectee->status() != InfectionStatus::Susceptible) return true;
        {
            std::stringstream ss;
            ss << "Place infection in place " << place->populationPos() << " group " << group
            << " from (" << infectorCell->index() << "," << infector->cellPos() << ") -> ("
            << infecteeCell->index() << "," << infectee->cellPos() << ")";
            LOG << LOG_LEVEL_DEBUG << ss.str();
        }
        infecteeCell->enqueuePerson(infectee->cellPos());
        m_counter++;
        return true;
    }

    double PlaceSweep::calcPlaceInf(
        Place*,
        Person* infector,
        const unsigned short int,
        size_t place_group)
    {
        double group_mul = (place_group < N_PLACE_GROUPS ?
            static_cast<double>(m_cfg->infectionConfig->meanPlaceGroupSize[place_group]) :
            1.0);
        return m_cfg->infectionConfig->placeTransmission *
            static_cast<double>(infector->params().infectiousness) / group_mul;
    }

    double PlaceSweep::calcPlaceFoi(
        Place* place,
        Person* infector,
        Person* /*infectee*/,
        const unsigned short int timestep,
        size_t group)
    {
        return calcPlaceInf(place, infector, timestep, group);
    }


} // namespace epiabm


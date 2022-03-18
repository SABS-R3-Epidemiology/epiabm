
#include "host_progression_sweep.hpp"
#include "../logfile.hpp"

#include <memory>
#include <random>
#include <climits>

namespace epiabm
{

    HostProgressionSweep::HostProgressionSweep(SimulationConfigPtr cfg) : SweepInterface(cfg)
    {
        std::random_device rd;
        m_generator = std::mt19937(rd());
        loadTransitionMatrix();
        loadTransitionTimeMatrix();
    }

    void HostProgressionSweep::operator()(const unsigned short timestep)
    {
        LOG << LOG_LEVEL_DEBUG << "Beginning Host Progression Sweep " << timestep;
        m_population->forEachCell(std::bind(
            &HostProgressionSweep::cellCallback, this,
            timestep, std::placeholders::_1));
        LOG << LOG_LEVEL_DEBUG << "Finished Host Progression Sweep " << timestep;
    }

    bool HostProgressionSweep::cellCallback(
        const unsigned short timestep, Cell *cell)
    {
        cell->forEachInfectious(std::bind(
            &HostProgressionSweep::cellInfectiousCallback, this,
            timestep, cell, std::placeholders::_1));
        cell->forEachExposed(std::bind(
            &HostProgressionSweep::cellExposedCallback, this,
            timestep, cell, std::placeholders::_1));
        return true;
    }

    bool HostProgressionSweep::cellExposedCallback(
        const unsigned short timestep, Cell *cell, Person *person)
    {
        if (timestep >= person->params().next_status_time)
        {
            if (person->status() != InfectionStatus::Exposed)
                LOG << LOG_LEVEL_ERROR << "Person " << person->cellPos() << " in cell " << cell->index() << " marked as exposed, but status was " << status_string(person->status());
            // Choose the person's first infectious status and update
            InfectionStatus firstStatus = chooseNextStatus(InfectionStatus::Exposed);
            person->updateStatus(cell, firstStatus, timestep);

            // Chose the person's next status and next status time
            person->params().next_status = chooseNextStatus(firstStatus);
            person->params().next_status_time = static_cast<unsigned short>(timestep +
                                                                            chooseNextTransitionTime(person->status(), person->params().next_status));

            // Move person from exposed to infectious
            cell->markInfectious(person->cellPos());
        }
        return true;
    }

    bool HostProgressionSweep::cellInfectiousCallback(
        const unsigned short timestep, Cell *cell, Person *person)
    {
        if (timestep > person->params().next_status_time)
        {
            // Update the person's state
            person->updateStatus(cell, person->params().next_status, timestep);
            if (person->status() == InfectionStatus::Recovered)
            {
                cell->markRecovered(person->cellPos());
                return true;
            }
            if (person->status() == InfectionStatus::Dead)
            {
                cell->markDead(person->cellPos());
                return true;
            }

            // Choose the next state and next time
            person->params().next_status = chooseNextStatus(person->status());
            person->params().next_status_time = static_cast<unsigned short>(timestep +
                                                                            chooseNextTransitionTime(person->status(), person->params().next_status));
        }
        return true;
    }

    InfectionStatus HostProgressionSweep::chooseNextStatus(InfectionStatus current)
    {
        size_t index = static_cast<size_t>(current);
        std::discrete_distribution<size_t> d(m_transitionMatrix[index].begin(), m_transitionMatrix[index].end());
        return static_cast<InfectionStatus>(d(m_generator));
    }

    unsigned short HostProgressionSweep::chooseNextTransitionTime(InfectionStatus current, InfectionStatus next)
    {
        size_t cindex = static_cast<size_t>(current);
        size_t nindex = static_cast<size_t>(next);
        if (current == InfectionStatus::Dead || current == InfectionStatus::Recovered)
            return USHRT_MAX;
        if (m_transitionTimeMatrix[cindex][nindex] == nullptr)
        {
            LOG << LOG_LEVEL_ERROR << "No transition time ICDF for " << status_string(current) << " -> " << status_string(next);
            return 0;
        }
        return m_transitionTimeMatrix[cindex][nindex]->choose(m_cfg->timestepsPerDay);
    }

    void HostProgressionSweep::loadTransitionMatrix()
    {
        const auto set = [&](InfectionStatus from, InfectionStatus to, double rate)
        {
            m_transitionMatrix[static_cast<size_t>(from)][static_cast<size_t>(to)] = rate;
        };
        set(InfectionStatus::Susceptible, InfectionStatus::Exposed, 1);
        set(InfectionStatus::Exposed, InfectionStatus::InfectASympt, 0.34);
        set(InfectionStatus::Exposed, InfectionStatus::InfectMild, 0.410061048258529);
        set(InfectionStatus::Exposed, InfectionStatus::InfectGP, 0.249938951741471);
        set(InfectionStatus::InfectASympt, InfectionStatus::Recovered, 1);
        set(InfectionStatus::InfectMild, InfectionStatus::Recovered, 1);
        set(InfectionStatus::InfectGP, InfectionStatus::Recovered, 0.837111575271931);
        set(InfectionStatus::InfectGP, InfectionStatus::InfectHosp, 0.162888424728069);
        set(InfectionStatus::InfectHosp, InfectionStatus::Recovered, 0.44166691836952);
        set(InfectionStatus::InfectHosp, InfectionStatus::InfectICU, 0.3969284544);
        set(InfectionStatus::InfectHosp, InfectionStatus::Dead, 0.161404627229571);
        set(InfectionStatus::InfectICU, InfectionStatus::InfectICURecov, 0.4765104);
        set(InfectionStatus::InfectICU, InfectionStatus::Dead, 0.5234896);
        set(InfectionStatus::InfectICURecov, InfectionStatus::Recovered, 1);
        set(InfectionStatus::Recovered, InfectionStatus::Recovered, 1);
        set(InfectionStatus::Dead, InfectionStatus::Dead, 1);
    }

    void HostProgressionSweep::loadTransitionTimeMatrix()
    {
        auto &cfg = m_cfg->infectionConfig->hostProgressionConfig;
        for (size_t i = 0; i < m_transitionTimeMatrix.size(); i++)
            m_transitionTimeMatrix[i].fill(nullptr);
        const auto set = [&](InfectionStatus from, InfectionStatus to, InverseCDF *icdf)
        {
            m_transitionTimeMatrix[static_cast<size_t>(from)][static_cast<size_t>(to)] = icdf;
        };
        set(InfectionStatus::Exposed, InfectionStatus::InfectASympt, &cfg->latentPeriodICDF);
        set(InfectionStatus::Exposed, InfectionStatus::InfectMild, &cfg->latentPeriodICDF);
        set(InfectionStatus::Exposed, InfectionStatus::InfectGP, &cfg->latentPeriodICDF);
        set(InfectionStatus::InfectASympt, InfectionStatus::Recovered, &cfg->asymptToRecovICDF);
        set(InfectionStatus::InfectMild, InfectionStatus::Recovered, &cfg->mildToRecovICDF);
        set(InfectionStatus::InfectGP, InfectionStatus::Recovered, &cfg->gpToRecovICDF);
        set(InfectionStatus::InfectGP, InfectionStatus::InfectHosp, &cfg->gpToHospICDF);
        set(InfectionStatus::InfectGP, InfectionStatus::Dead, &cfg->gpToDeathICDF);
        set(InfectionStatus::InfectHosp, InfectionStatus::Recovered, &cfg->hospToRecovICDF);
        set(InfectionStatus::InfectHosp, InfectionStatus::InfectICU, &cfg->hospToICUICDF);
        set(InfectionStatus::InfectHosp, InfectionStatus::Dead, &cfg->hospToDeathICDF);
        set(InfectionStatus::InfectICU, InfectionStatus::InfectICURecov, &cfg->icuToICURecovICDF);
        set(InfectionStatus::InfectICU, InfectionStatus::Dead, &cfg->icuToDeathICDF);
        set(InfectionStatus::InfectICURecov, InfectionStatus::Recovered, &cfg->icuRecovToRecovICDF);
    }

} // namespace epiabm

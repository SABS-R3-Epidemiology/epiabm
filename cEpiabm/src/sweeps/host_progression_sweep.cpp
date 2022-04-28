
#include "host_progression_sweep.hpp"
#include "../logfile.hpp"

#include <memory>
#include <random>
#include <climits>
#include <exception>
#include <math.h>
#include <cmath>

namespace epiabm
{

    HostProgressionSweep::HostProgressionSweep(SimulationConfigPtr cfg) : SweepInterface(cfg)
    {
        loadTransitionMatrix();
        loadTransitionTimeMatrix();
        loadInfectiousnessProfile();
        m_initialInfectiousnessDistrib = std::gamma_distribution<double>(1.0, 1.0);
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
            InfectionStatus firstStatus = chooseNextStatus(person, InfectionStatus::Exposed);
            person->updateStatus(cell, firstStatus, timestep);
            person->params().infection_start_timestep = timestep;
            person->params().initial_infectiousness = static_cast<float>(chooseInfectiousness(firstStatus));

            // Chose the person's next status and next status time
            person->params().next_status = chooseNextStatus(person, firstStatus);
            person->params().next_status_time = static_cast<unsigned short>(timestep +
                                                                            chooseNextTransitionTime(person->status(), person->params().next_status));

            // Move person from exposed to infectious
            cell->markInfectious(person->cellPos());
            updateInfectiousness(timestep, person);
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
            person->params().next_status = chooseNextStatus(person, person->status());
            person->params().next_status_time = static_cast<unsigned short>(timestep +
                                                                            chooseNextTransitionTime(person->status(), person->params().next_status));
        }
        updateInfectiousness(timestep, person);
        return true;
    }

    InfectionStatus HostProgressionSweep::chooseNextStatus(Person* person, InfectionStatus current)
    {
        size_t index = static_cast<size_t>(current);
        std::discrete_distribution<size_t> d(m_transitionMatrix[person->params().age_group][index].begin(), m_transitionMatrix[person->params().age_group][index].end());
        return static_cast<InfectionStatus>(d(
            m_cfg->randomManager->g().generator()));
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
        return m_transitionTimeMatrix[cindex][nindex]->choose(
            m_cfg->timestepsPerDay, m_cfg->randomManager->g().generator());
    }

    double HostProgressionSweep::chooseInfectiousness(InfectionStatus status)
    {
        double initialInfectiousness = m_initialInfectiousnessDistrib(m_cfg->randomManager->g().generator());
        if (status == InfectionStatus::InfectASympt)
            return m_cfg->infectionConfig->asymptInfectiousness * initialInfectiousness;
        else if (status == InfectionStatus::InfectMild || status == InfectionStatus::InfectGP)
            return m_cfg->infectionConfig->symptInfectiousness * initialInfectiousness;
        else
        {
            std::stringstream ss;
            ss << "Cannot choose infectiousness for " << status_string(status) << ", Invalid First Infective Status";
            std::throw_with_nested(std::runtime_error(ss.str()));
        }
    }

    void HostProgressionSweep::updateInfectiousness(const unsigned short timestep, Person* person)
    {
        if (person->params().infection_start_timestep > timestep) std::throw_with_nested(std::runtime_error("Spatial Sweep: Infection start time cannot be later than current timestep"));
        const unsigned short t = static_cast<unsigned short>(timestep - person->params().infection_start_timestep);
        if (t >= m_infectiousnessProfile.size()) std::throw_with_nested(std::runtime_error("Spatial Sweep: Time since infection start too large to scale"));
        person->params().infectiousness = person->params().initial_infectiousness * static_cast<float>(m_infectiousnessProfile[t]);
    }

    void HostProgressionSweep::loadTransitionMatrix()
    {
        LOG << LOG_LEVEL_NORMAL << "Host Progression Sweep: Loading Transition State Matrix";
        const auto set = [&](InfectionStatus from, InfectionStatus to, double value)
        {
            for (size_t i = 0; i < N_AGE_GROUPS; i++)
            {
                m_transitionMatrix[i][static_cast<size_t>(from)][static_cast<size_t>(to)] = value;
            }
        };
        const auto setValues = [&](InfectionStatus from, InfectionStatus to, std::array<double, N_AGE_GROUPS> rates)
        {
            if (m_cfg->infectionConfig->hostProgressionConfig->use_ages)
                for (size_t i = 0; i < N_AGE_GROUPS; i++)
                {
                    m_transitionMatrix[i][static_cast<size_t>(from)][static_cast<size_t>(to)] = rates[i];
                }
            else
            {
                double sAgeDistrib = std::accumulate(m_cfg->populationConfig->age_proportions.begin(),
                    m_cfg->populationConfig->age_proportions.end(), 0);
                double value = 0;
                for (size_t i = 0; i < N_AGE_GROUPS; i++)
                {
                    value += rates[i] * m_cfg->populationConfig->age_proportions[i] / sAgeDistrib;
                }
                value /= N_AGE_GROUPS;
                set(from, to, value);
                LOG << LOG_LEVEL_NORMAL << "Transition state for " << status_string(from) << " -> " << status_string(to) << " = " << value << " (Weighted average since configured to not use ages)";
            }
        };
        HostProgressionConfigPtr cfg = m_cfg->infectionConfig->hostProgressionConfig;
        set(InfectionStatus::Susceptible, InfectionStatus::Exposed, 1);
        setValues(InfectionStatus::Exposed, InfectionStatus::InfectASympt, cfg->prob_exposed_to_asympt);
        setValues(InfectionStatus::Exposed, InfectionStatus::InfectMild, cfg->prob_exposed_to_mild);
        setValues(InfectionStatus::Exposed, InfectionStatus::InfectGP, cfg->prob_exposed_to_gp);
        set(InfectionStatus::InfectASympt, InfectionStatus::Recovered, 1);
        set(InfectionStatus::InfectMild, InfectionStatus::Recovered, 1);
        setValues(InfectionStatus::InfectGP, InfectionStatus::Recovered, cfg->prob_gp_to_recov);
        setValues(InfectionStatus::InfectGP, InfectionStatus::InfectHosp, cfg->prob_gp_to_hosp);
        setValues(InfectionStatus::InfectHosp, InfectionStatus::Recovered, cfg->prob_hosp_to_recov);
        setValues(InfectionStatus::InfectHosp, InfectionStatus::InfectICU, cfg->prob_hosp_to_icu);
        setValues(InfectionStatus::InfectHosp, InfectionStatus::Dead, cfg->prob_hosp_to_death);
        setValues(InfectionStatus::InfectICU, InfectionStatus::InfectICURecov, cfg->prob_icu_to_icurecov);
        setValues(InfectionStatus::InfectICU, InfectionStatus::Dead, cfg->prob_icu_to_death);
        set(InfectionStatus::InfectICURecov, InfectionStatus::Recovered, 1);
        set(InfectionStatus::Recovered, InfectionStatus::Recovered, 1);
        set(InfectionStatus::Dead, InfectionStatus::Dead, 1);
        LOG << LOG_LEVEL_NORMAL << "Host Progression Sweep: Finished Loading Transition State Matrix";
    }

    void HostProgressionSweep::loadTransitionTimeMatrix()
    {
        LOG << LOG_LEVEL_NORMAL << "Host Progression Sweep: Loading Transition Time Matrix";
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
        LOG << LOG_LEVEL_NORMAL << "Host Progression Sweep: Finished Loading Transition Time Matrix";
    }

    void HostProgressionSweep::loadInfectiousnessProfile()
    {
        LOG << LOG_LEVEL_NORMAL << "Host Progression Sweep: Loading Infectiousness Profile";

        double timestep = 1.0 / static_cast<double>(m_cfg->timestepsPerDay);
        auto& cfg = m_cfg->infectionConfig->hostProgressionConfig;
        size_t profileResolution = cfg->infectiousness_profile.size() - 1;
        double profileAverage = std::accumulate(cfg->infectiousness_profile.begin(), cfg->infectiousness_profile.end(), 0) / static_cast<double>(profileResolution + 1);

        const size_t maxInfectiousSteps = 2550;
        size_t nInfectiousSteps = static_cast<size_t>(ceil(cfg->asymptToRecovICDF.mean() / timestep));
        if (nInfectiousSteps > maxInfectiousSteps)
            std::throw_with_nested(std::runtime_error(
                "Timestep is too small for Infectious duration."));

        m_infectiousnessProfile = std::vector<double>(maxInfectiousSteps, 0);
        for (size_t i = 0; i < nInfectiousSteps; i++)
        {
            double t = (static_cast<double>(i) * timestep / cfg->asymptToRecovICDF.mean()) * static_cast<double>(profileResolution);
            size_t associatedProfileIndex = static_cast<size_t>(t);
            t -= static_cast<double>(associatedProfileIndex);

            if (associatedProfileIndex < profileResolution)
                m_infectiousnessProfile[i] = 
                    cfg->infectiousness_profile[associatedProfileIndex] * (1-t) +
                    cfg->infectiousness_profile[associatedProfileIndex+1] * t;
            else
                m_infectiousnessProfile[i] = cfg->infectiousness_profile[profileResolution];
        }

        for (size_t i = 0; i < nInfectiousSteps; i++)
            m_infectiousnessProfile[i] /= profileAverage;

        LOG << LOG_LEVEL_NORMAL << "Host Progression Sweep: Finished Loading Infectiousness Profile";
    }

} // namespace epiabm

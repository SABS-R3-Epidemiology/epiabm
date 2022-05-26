
#include "cell.hpp"

#include <iostream>
#include <algorithm>
#include <iterator>
#include <random>
#include <exception>
#include <stdexcept>

namespace epiabm
{

    Cell::Cell(size_t index) :
        m_index(index),
        m_location(),
        m_people(),
        m_microcells(),
        m_personQueue(),
        m_peopleInQueue(),
        //m_peopleSorted(),
        //m_peopleSortedInv(),
        //m_numInfectious(0)
        m_infectiousPeople(),
        m_susceptiblePeople(),
        m_exposedPeople(),
        m_recoveredPeople(),
        m_deadPeople(),
        m_compartmentCounter()
    {}

    Cell::~Cell()
    {
        //std::cout << "Deleted Cell" << std::endl;
    }

    size_t Cell::index() const { return m_index; }

    void Cell::forEachMicrocell(std::function<bool(Microcell*)> callback)
    {
        for (size_t i = 0; i < m_microcells.size(); i++)
        {
            if (!callback(&m_microcells[i])) return;
        }
    }

    void Cell::forEachPerson(std::function<bool(Person*)> callback)
    {
        for (size_t i = 0; i < m_people.size(); i++)
        {
            if (!callback(&m_people[i])) return;
        }
    }

    void Cell::forEachInfectious(std::function<bool(Person*)> callback)
    {
        /*for (size_t i = 0; i < m_numInfectious; i++)
        {
            if (!callback(&m_people[m_peopleSorted[i]])) return;
        }*/
        std::set<size_t> set = m_infectiousPeople;
        for (auto it = set.begin(); it != set.end(); ++it)
            if (!callback(&m_people[*it])) return;
    }

    void Cell::forEachNonInfectious(std::function<bool(Person*)> callback)
    {
        /*for (size_t i = m_numInfectious; i < m_people.size(); i++)
        {
            if (!callback(&m_people[m_peopleSorted[i]])) return;
        }*/
        std::set<size_t> set = m_susceptiblePeople;
        for (auto it = set.begin(); it != set.end(); ++it)
            if (!callback(&m_people[*it])) return;
    }

    void Cell::forEachExposed(std::function<bool(Person*)> callback)
    {
        std::set<size_t> set = m_exposedPeople;
        for (auto it = set.begin(); it != set.end(); ++it)
            if (!callback(&m_people[*it])) return;
    }

    Person& Cell::getPerson(size_t i) { return m_people[i]; }
    Microcell& Cell::getMicrocell(size_t i) { return m_microcells[i]; }

    /**
     * @brief Apply Callback to each person in Queue
     * Also Clears the queue
     * @param callback
     */
    void Cell::processQueue(std::function<void(size_t)> callback)
    {
        while (!m_personQueue.empty()) // loop through queue
        {
            callback(m_personQueue.front());
            m_personQueue.pop();
        }
        m_peopleInQueue.clear(); // Remove person from the set of people currently in queue
    }

    /**
     * @brief Add person to queue
     * Same person cannot be queued twice.
     * @param personIndex
     * @return true Person successfully queued.
     * @return false Person reject because already in queue.
     */
    bool Cell::enqueuePerson(size_t personIndex)
    {
        if (personIndex >= m_people.size()) throw std::runtime_error("Attempted to queue index out of range");
        if (m_peopleInQueue.find(personIndex) != m_peopleInQueue.end()) return false; // if person already queued
        m_personQueue.push(personIndex); // add to queue
        m_peopleInQueue.insert(personIndex); // insert into queued set
        return true;
    }

    std::vector<Person>& Cell::people() { return m_people; }
    std::vector<Microcell>& Cell::microcells() { return m_microcells; }

    /**
     * @brief Initialize framework for fast looping through infectious / susceptible
     * Cell can maintain a vector of people where all the infectious are at the start.
     * This is to allow quick looping through only infectious people without looping through all people and checking their status.
     */
    void Cell::initializeInfectiousGrouping()
    {
        /*m_peopleSorted = std::vector<size_t>(m_people.size());
        m_peopleSortedInv = std::vector<size_t>(m_people.size());
        for (size_t i = 0; i < m_people.size(); i++)
        {
            m_peopleSortedInv[i] = i;
            m_peopleSorted[i] = i;
        }*/
        m_susceptiblePeople.clear();
        m_exposedPeople.clear();
        m_infectiousPeople.clear();
        m_recoveredPeople.clear();
        m_deadPeople.clear();
        for (size_t i = 0; i < m_people.size(); i++)
        {
            if (m_people[i].status() == InfectionStatus::Susceptible) m_susceptiblePeople.insert(i);
            else if (m_people[i].status() == InfectionStatus::Exposed) m_exposedPeople.insert(i);
            else if (m_people[i].status() == InfectionStatus::Recovered) m_recoveredPeople.insert(i);
            else if (m_people[i].status() == InfectionStatus::Dead) m_deadPeople.insert(i);
            else m_infectiousPeople.insert(i);
        }
    }

    /**
     * @brief Mark Person as Infectious for Fast Looping through Infectious People
     * Mark a person as infectious. Used for fast looping through infectious or non-infectious people without looping through all people and checking their statuses.
     * Cell::initializeInfectiousGroupings must have been called once before for this function to be used.
     * @param newInfected Person who is becoming infectious.
     * @return true Successfully changed person's state to infectious.
     * @return false Person was already infectious.
     */
    bool Cell::markInfectious(size_t newInfected)
    {
        /*if (m_peopleSortedInv[newInfected] < m_numInfectious) return false; // Person already in infected section
        size_t swapTarget = m_peopleSorted[m_numInfectious]; // Index of swap target in m_people

        std::swap(m_peopleSorted[m_peopleSortedInv[newInfected]],
            m_peopleSorted[m_numInfectious]); // Swap new infected and target in sorted vector
        m_peopleSortedInv[swapTarget] = m_peopleSortedInv[newInfected]; // New location of target in sorted = old position of newly infected
        m_peopleSortedInv[newInfected] = m_numInfectious; // New location of newly infected is m_numInfected;

        m_numInfectious++; // Increment number of infected
        return true;*/
        if (m_infectiousPeople.find(newInfected) != m_infectiousPeople.end()) return false;
        m_susceptiblePeople.erase(newInfected);
        m_infectiousPeople.insert(newInfected);
        m_exposedPeople.erase(newInfected);
        return true;
    }

    /**
     * @brief Mark Person as Non-Infectious for Fast Looping through Infectious People
     * Mark a person as non-infectious. Used for fast looping through infectious or non-infectious people without looping through all people and checking their statuses.
     * Cell::initializeInfectiousGroupings must have been called once before this can be used.
     * @param oldInfected Person who is no longer infectious.
     * @return true Successfully changed person's state to non-infectious.
     * @return false Person was already marked as non-infectious.
     */
    bool Cell::markNonInfectious(size_t oldInfected)
    {
        /*if (m_peopleSortedInv[oldInfected] >= m_numInfectious) return false; // Person already in non-infected
        size_t swapTarget = m_peopleSorted[m_numInfectious - 1]; // Index of swap target (last infectious person)

        std::swap(m_peopleSorted[m_peopleSortedInv[oldInfected]],
            m_peopleSorted[m_numInfectious - 1]);
        m_peopleSortedInv[swapTarget] = m_peopleSortedInv[oldInfected]; // New location of swap target is old position of previously infected
        m_peopleSortedInv[oldInfected] = m_numInfectious - 1;

        m_numInfectious--;
        return true;*/
        if (m_susceptiblePeople.find(oldInfected) != m_susceptiblePeople.end()) return false;
        m_susceptiblePeople.insert(oldInfected);
        m_infectiousPeople.erase(oldInfected);
        m_exposedPeople.erase(oldInfected);
        return true;
    }

    bool Cell::markExposed(size_t newInfected)
    {
        if (m_exposedPeople.find(newInfected) != m_exposedPeople.end()) return false;
        m_susceptiblePeople.erase(newInfected);
        m_infectiousPeople.erase(newInfected);
        m_exposedPeople.insert(newInfected);
        return true;
    }

    bool Cell::markDead(size_t person)
    {
        if (m_deadPeople.find(person) != m_deadPeople.end()) return false;
        m_deadPeople.insert(person);
        m_infectiousPeople.erase(person);
        m_exposedPeople.erase(person);
        m_susceptiblePeople.erase(person);
        return true;
    }

    bool Cell::markRecovered(size_t person)
    {
        if (m_recoveredPeople.find(person) != m_recoveredPeople.end()) return false;
        m_recoveredPeople.insert(person);
        m_infectiousPeople.erase(person);
        m_exposedPeople.erase(person);
        m_susceptiblePeople.erase(person);
        return true;
    }

    size_t Cell::numSusceptible() const
    {
        return m_susceptiblePeople.size();
    }

    /**
     * @brief Get Number of Infectious
     * Get number of currently infectious people.
     * This corresponds to the number of infectious being maintained by the cell for fast looping through infectious / non-infectious.
     * Cell::initializeInfectiousGroupings() must have been called once before this can be used.
     * @return size_t Number of infectious
     */
    size_t Cell::numInfectious() const
    {
        //return m_numInfectious;
        return m_infectiousPeople.size();
    }

    size_t Cell::numExposed() const
    {
        return m_exposedPeople.size();
    }
    
    size_t Cell::numRecovered() const
    {
        return m_recoveredPeople.size();
    }

    size_t Cell::numDead() const
    {
        return m_deadPeople.size();
    }

    bool Cell::sampleInfectious(size_t n, std::function<void(Person*)> callback)
    {
        if (m_infectiousPeople.size() < 1){
            return false;
        }
        std::vector<size_t> sampled = std::vector<size_t>();
        std::sample(m_infectiousPeople.begin(), m_infectiousPeople.end(),
            std::back_inserter(sampled), n, std::mt19937{std::random_device{}()});
        for (const auto& s : sampled)
            callback(&m_people[s]);
        return true;
    }

    bool Cell::sampleSusceptible(size_t n, std::function<void(Person*)> callback)
    {
        if (m_susceptiblePeople.size() < 1){
            return false;
        }
        std::vector<size_t> sampled = std::vector<size_t>();
        std::sample(m_susceptiblePeople.begin(),m_susceptiblePeople.end(),
            std::back_inserter(sampled), n, std::mt19937{std::random_device{}()});
        for (const auto& s : sampled)
            callback(&m_people[s]);
        return true;
    }

    void Cell::initialize()
    {
        initializeInfectiousGrouping();
        m_compartmentCounter.initialize(m_people);
        for (auto& mc : m_microcells)
        {
            mc.initialize(this);
        }
    }

    unsigned int Cell::compartmentCount(InfectionStatus status)
    {
        return m_compartmentCounter(status);
    }

    void Cell::setLocation(std::pair<double, double> loc)
    {
        m_location = loc;
    }
        
    std::pair<double, double> Cell::location() const
    {
        return m_location;
    }

    void Cell::personStatusChange(Person* person, InfectionStatus newStatus, unsigned short timestep)
    {
        m_compartmentCounter.notify(person->status(), newStatus);
        m_microcells[person->microcell()].personStatusChange(person, newStatus, timestep);
    }

} // namespace epiabm

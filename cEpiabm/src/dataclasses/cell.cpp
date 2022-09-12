
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

    /**
     * @brief Apply callback on each microcell in cell
     * 
     * Callback function can return false to terminate loop early.
     * 
     * @param callback Callback function applied to each microcell
     */
    void Cell::forEachMicrocell(std::function<bool(Microcell*)> callback)
    {
        for (size_t i = 0; i < m_microcells.size(); i++)
        {
            if (!callback(&m_microcells[i])) return;
        }
    }

    /**
     * @brief Apply callback on each person in cell
     * 
     * Callback function can return false to terminate loop early
     * 
     * @param callback Callback function to apply to each person
     */
    void Cell::forEachPerson(std::function<bool(Person*)> callback)
    {
        for (size_t i = 0; i < m_people.size(); i++)
        {
            if (!callback(&m_people[i])) return;
        }
    }

    /**
     * @brief Apply callback on each infectious person in the cell
     * 
     * Callback function can return false to terminate loop early
     * 
     * @param callback Callback function to apply to each infectious person
     */
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

    /**
     * @brief Apply callback on each non-infectious person in the cell
     * 
     * Callback function can return false to terminate loop early
     * 
     * @param callback Callback function to apply to each non-infectious person
     */
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

    /**
     * @brief Apply callback on each exposed person in the cell
     * 
     * Callback function can return false to terminate loop early
     * 
     * @param callback Callback function to apply to each exposed person
     */
    void Cell::forEachExposed(std::function<bool(Person*)> callback)
    {
        std::set<size_t> set = m_exposedPeople;
        for (auto it = set.begin(); it != set.end(); ++it)
            if (!callback(&m_people[*it])) return;
    }

    /**
     * @brief Retrieve ith person in cell
     * 
     * @param i Index of person to retrieve
     * @return Person& Reference to ith person
     */
    Person& Cell::getPerson(size_t i) { return m_people[i]; }
    /**
     * @brief Retrieve ith microcell in cell
     * 
     * @param i Index of microcell to retrieve
     * @return Microcell& Reference to ith microcell
     */
    Microcell& Cell::getMicrocell(size_t i) { return m_microcells[i]; }

    void Cell::processQueue(std::function<void(size_t)> callback)
    {
        std::lock_guard<std::mutex> l(m_queueMutex);
        while (!m_personQueue.empty()) // loop through queue
        {
            callback(m_personQueue.front());
            m_personQueue.pop();
        }
        m_peopleInQueue.clear(); // Remove person from the set of people currently in queue
    }

    /**
     * @brief Add person to the cell's queue
     * Used for applying new infections at the end of all infection transmitting sweeps
     * 
     * Same person cannot be added twice
     * Returns true if person was successfully added
     * 
     * @param personIndex Index of person to enqueue
     * @return true Returns true if successfully enqueued
     * @return false Returns false if unable to enqueue person (person already queued)
     */
    bool Cell::enqueuePerson(size_t personIndex)
    {
        std::lock_guard<std::mutex> l(m_queueMutex);
        if (personIndex >= m_people.size()) throw std::runtime_error("Attempted to queue index out of range");
        if (m_peopleInQueue.find(personIndex) != m_peopleInQueue.end()) return false; // if person already queued
        m_personQueue.push(personIndex); // add to queue
        m_peopleInQueue.insert(personIndex); // insert into queued set
        return true;
    }

    /**
     * @brief Reference to cell's people vector
     * 
     * @return std::vector<Person>& Reference to people vector
     */
    std::vector<Person>& Cell::people() { return m_people; }
    /**
     * @brief Reference to cell's microcells vector
     * 
     * @return std::vector<Microcell>& Reference to microcells vector
     */
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
        std::lock_guard<std::mutex> l(m_markMutex);
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
        std::lock_guard<std::mutex> l(m_markMutex);
        if (m_susceptiblePeople.find(oldInfected) != m_susceptiblePeople.end()) return false;
        m_susceptiblePeople.insert(oldInfected);
        m_infectiousPeople.erase(oldInfected);
        m_exposedPeople.erase(oldInfected);
        return true;
    }

    /**
     * @brief Mark person as exposed
     * 
     * @param newInfected Index of newly infected person
     * @return true Returns true if successfully changed person's state
     * @return false Returns false if person already marked as exposed
     */
    bool Cell::markExposed(size_t newInfected)
    {
        std::lock_guard<std::mutex> l(m_markMutex);
        if (m_exposedPeople.find(newInfected) != m_exposedPeople.end()) return false;
        m_susceptiblePeople.erase(newInfected);
        m_infectiousPeople.erase(newInfected);
        m_exposedPeople.insert(newInfected);
        return true;
    }

    /**
     * @brief Mark person as dead
     * 
     * @param person Index of dead person
     * @return true Returns true if successfully changed person's state
     * @return false Returns false if person already marked as dead
     */
    bool Cell::markDead(size_t person)
    {
        std::lock_guard<std::mutex> l(m_markMutex);
        if (m_deadPeople.find(person) != m_deadPeople.end()) return false;
        m_deadPeople.insert(person);
        m_infectiousPeople.erase(person);
        m_exposedPeople.erase(person);
        m_susceptiblePeople.erase(person);
        return true;
    }

    /**
     * @brief Mark person as recovered
     * 
     * @param person Index of recovered person
     * @return true Returns true if successfully changed person's state
     * @return false Returns false if person already marked as recovered
     */
    bool Cell::markRecovered(size_t person)
    {
        std::lock_guard<std::mutex> l(m_markMutex);
        if (m_recoveredPeople.find(person) != m_recoveredPeople.end()) return false;
        m_recoveredPeople.insert(person);
        m_infectiousPeople.erase(person);
        m_exposedPeople.erase(person);
        m_susceptiblePeople.erase(person);
        return true;
    }

    /**
     * @brief Get number of susceptible people
     * 
     * @return size_t Number of susceptible people
     */
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

    /**
     * @brief Get number of people marked as exposed
     * 
     * @return size_t Number of exposed people
     */
    size_t Cell::numExposed() const
    {
        return m_exposedPeople.size();
    }
    
    /**
     * @brief Get number of people marked as recovered
     * 
     * @return size_t Number of recovered people
     */
    size_t Cell::numRecovered() const
    {
        return m_recoveredPeople.size();
    }

    /**
     * @brief Get number of people marked as dead
     * 
     * @return size_t Number of dead people
     */
    size_t Cell::numDead() const
    {
        return m_deadPeople.size();
    }

    /**
     * @brief Randomly sample n infectious people in the cell
     * 
     * If n is larger than number of infectious people, all infectious people are returned
     * 
     * @param n Number of people to sample
     * @param callback Callback applied to each chosen person
     * @param rg Random number generator to use
     * @return true Success
     * @return false Returns false if there are no infectious people to sample
     */
    bool Cell::sampleInfectious(size_t n, std::function<void(Person*)> callback, std::mt19937_64& rg)
    {
        if (m_infectiousPeople.size() < 1){
            return false;
        }
        std::vector<size_t> sampled = std::vector<size_t>();
        std::sample(m_infectiousPeople.begin(), m_infectiousPeople.end(),
            std::back_inserter(sampled), n, rg);
        for (const auto& s : sampled)
            callback(&m_people[s]);
        return true;
    }

    /**
     * @brief Randomly sample n susceptible people in the cell
     * 
     * If n is larger than number of susceptible people, all susceptible people are returned
     * 
     * @param n Number of people to sample
     * @param callback Callback to apply to each sampled person
     * @param rg Random generator to use
     * @return true Success
     * @return false Returns false if there are no susceptible people to sample
     */
    bool Cell::sampleSusceptible(size_t n, std::function<void(Person*)> callback, std::mt19937_64& rg)
    {
        if (m_susceptiblePeople.size() < 1){
            return false;
        }
        std::vector<size_t> sampled = std::vector<size_t>();
        std::sample(m_susceptiblePeople.begin(),m_susceptiblePeople.end(),
            std::back_inserter(sampled), n, rg);
        for (const auto& s : sampled)
            callback(&m_people[s]);
        return true;
    }

    /**
     * @brief Initialize the cell
     * 
     * Automatically called by Population::initialize() as part of the population setup procedure
     * 
     */
    void Cell::initialize()
    {
        initializeInfectiousGrouping();
        m_compartmentCounter.initialize(m_people);
        for (auto& mc : m_microcells)
        {
            mc.initialize(this);
        }
    }

    /**
     * @brief Retrieve number of people with specific InfectionStatus
     * 
     * @param status Compartment to retrieve
     * @return unsigned int Number of people in the compartment
     */
    unsigned int Cell::compartmentCount(InfectionStatus status)
    {
        return m_compartmentCounter(status);
    }

    /**
     * @brief Set the cell's location
     * 
     * Used for spatial sweep distance modifiers
     * 
     * @param loc Cell's location
     */
    void Cell::setLocation(std::pair<double, double> loc)
    {
        m_location = loc;
    }
    
    /**
     * @brief Get the cell's location
     * 
     * @return std::pair<double, double> Cell's location 
     */
    std::pair<double, double> Cell::location() const
    {
        return m_location;
    }

    /**
     * @brief Change a person's status
     * 
     * Automatically called by Person::updateStatus.
     * Should not be called manually
     * Part of person update status procedure
     * 
     * @param person Person to alter
     * @param newStatus Person's new status
     * @param timestep Time of status change
     */
    void Cell::personStatusChange(Person* person, InfectionStatus newStatus, unsigned short timestep)
    {
        m_compartmentCounter.notify(person->status(), newStatus);
        m_microcells[person->microcell()].personStatusChange(person, newStatus, timestep);
    }

} // namespace epiabm

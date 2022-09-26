#include "person.hpp"
#include "place.hpp"
#include "cell.hpp"
#include "population.hpp"

#include <iostream>
#include <exception>

namespace epiabm
{

    /**
     * @brief Construct a new Person:: Person object
     * 
     * @param microcell Index of parent microcell within parent cell's microcells vector
     * @param cellPos Index of person within parent cell's people vector
     * @param mcellPos Index of person within parent microcell's people vector
     */
    Person::Person(size_t microcell, size_t cellPos, size_t mcellPos) :
        m_status(InfectionStatus::Susceptible),
        m_params(PersonParams()),
        m_cellPos(cellPos),
        m_mcellPos(mcellPos),
        m_microcell(microcell),
        m_hasHousehold(false),
        m_places()
    {}

    /**
     * @brief Destroy the Person:: Person object
     * 
     */
    Person::~Person()
    {
        //std::cout << "Person Destructor" << std::endl;
    }

    /**
     * @brief Get person's infection status
     * 
     * @return InfectionStatus Person's infection status
     */
    InfectionStatus Person::status() const { return m_status; }
    /**
     * @brief Get person's parameters
     * 
     * Used to access and modify specific person's parameters
     * 
     * @return PersonParams& Reference to person's parameters struct
     */
    PersonParams& Person::params() { return m_params; }

    /**
     * @brief Force set status (For configuring population)
     * 
     * Population has to be re-initialized if this is called
     * 
     * @param status Person's new infection status
     */
    void Person::setStatus(const InfectionStatus status)
    {
        m_status = status;
    }

    /**
     * @brief Update a person's infection status
     * 
     * Use this method to update a person's infection status
     * 
     * @param cell Pointer to parent cell
     * @param status Person's new infection status
     * @param timestep Time of status change
     */
    void Person::updateStatus(Cell* cell, const InfectionStatus status, const unsigned short timestep)
    {
        cell->personStatusChange(this, status, timestep);
        m_status = status;
    }

    /**
     * @brief Get position of person within parent Cell's people vector
     * 
     * @return size_t Index of person within parent cell's people vector
     */
    size_t Person::cellPos() const { return m_cellPos; }
    /**
     * @brief Get position of person within parent microcell's people vector
     * 
     * @return size_t Index of person within parent microcell's people vector
     */
    size_t Person::microcellPos() const { return m_mcellPos; }
    /**
     * @brief Get index of person's microcell within parent cell's microcells vector
     * 
     * @return size_t Index of person's microcell within parent cell's microcell vector
     */
    size_t Person::microcell() const { return m_microcell; }

    /**
     * @brief Set person's household
     * 
     * @param hh Index of household in person's microcell
     * @return true Successfuly added person to household
     * @return false Failed, person is already part of a household
     */
    bool Person::setHousehold(size_t hh)
    {
        if (m_hasHousehold)
            return false;
        m_household = hh;
        m_hasHousehold = true;
        return true;
    }

    /**
     * @brief Retrieve index of person's houshold
     * 
     * @return std::optional<size_t> Index of household within person's microcell
     */
    std::optional<size_t> Person::household()
    { return m_hasHousehold? m_household : std::optional<size_t>(); }

    /**
     * @brief Add person to place
     * 
     * @param population Reference to parent population
     * @param cell Pointer to parent cell
     * @param place_index Index of place in population
     * @param group Place's group number
     */
    void Person::addPlace(Population& population, Cell* cell, size_t place_index, size_t group)
    {
        if (m_places.find(std::make_pair(place_index, group)) != m_places.end()) return;
        m_places.insert(std::make_pair(place_index, group));
        population.places()[place_index].addMember(cell->index(), m_cellPos, group);
    }

    /**
     * @brief Remove person from a specific place
     * 
     * Remove person from a specific place and group number.
     * 
     * @param population Reference to parent population
     * @param cell Pointer to parent cell
     * @param place_index Index of place in population
     * @param group Place's group number
     */
    void Person::removePlace(Population& population, Cell* cell, size_t place_index, size_t group)
    {
        std::pair<size_t, size_t> r = std::make_pair(place_index, group);
        if (m_places.find(r) == m_places.end()) return;
        m_places.erase(r);
        population.places()[place_index].removeMember(cell->index(), m_cellPos, group);
    }

    /**
     * @brief Remove person from place type
     * 
     * Removes person from all places (ignoring place group number)
     * 
     * @param population Reference to parent population
     * @param cell Pointer to parent cell
     * @param place_index Index of place in population
     */
    void Person::removePlaceAllGroups(Population& population, Cell* cell, size_t place_index)
    {
        for (auto it = m_places.begin(); it != m_places.end();)
        {
            if (it->first != place_index) ++it;
            else m_places.erase(it++);
        }
        population.places()[place_index].removeMemberAllGroups(cell->index(), m_cellPos);
    }

    /**
     * @brief Get reference to person's places set
     * 
     * Set of place indices which person is a member of.
     * Each entry is a pair of place's index within Population::m_places and place's group number.
     * Groups can be used to represent multiple places of the same type.
     * 
     * @return std::set<std::pair<size_t, size_t>>& Set of places which person is a member of 
     */
    std::set<std::pair<size_t, size_t>>& Person::places() { return m_places; }

    /**
     * @brief Loop through each place
     * Callback provides the place and group within place that the person is part of
     * 
     * @param population 
     * @param callback 
     */
    void Person::forEachPlace(Population& population, std::function<void(Place*, size_t)> callback)
    {
        for (const std::pair<size_t, size_t>& p : m_places)
            callback(&population.places()[p.first], p.second);
    }

} // namespace epiabm

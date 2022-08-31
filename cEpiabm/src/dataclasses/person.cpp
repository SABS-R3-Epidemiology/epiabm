#include "person.hpp"
#include "place.hpp"
#include "cell.hpp"
#include "population.hpp"

#include <iostream>
#include <exception>

namespace epiabm
{

    Person::Person(size_t microcell, size_t cellPos, size_t mcellPos) :
        m_status(InfectionStatus::Susceptible),
        m_params(PersonParams()),
        m_cellPos(cellPos),
        m_mcellPos(mcellPos),
        m_microcell(microcell),
        m_hasHousehold(false),
        m_places()
    {}

    Person::~Person()
    {
        //std::cout << "Person Destructor" << std::endl;
    }

    InfectionStatus Person::status() const { return m_status; }
    PersonParams& Person::params() { return m_params; }

    void Person::setStatus(const InfectionStatus status)
    {
        m_status = status;
    }

    void Person::updateStatus(Cell* cell, const InfectionStatus status, const unsigned short timestep)
    {
        cell->personStatusChange(this, status, timestep);
        m_status = status;
    }

    size_t Person::cellPos() const { return m_cellPos; }
    size_t Person::microcellPos() const { return m_mcellPos; }
    size_t Person::microcell() const { return m_microcell; }

    bool Person::setHousehold(size_t hh)
    {
        if (m_hasHousehold)
            return false;
        m_household = hh;
        m_hasHousehold = true;
        return true;
    }

    std::optional<size_t> Person::household()
    { return m_hasHousehold? m_household : std::optional<size_t>(); }

    void Person::addPlace(Population& population, Cell* cell, size_t place_index, size_t group)
    {
        if (m_places.find(std::make_pair(place_index, group)) != m_places.end()) return;
        m_places.insert(std::make_pair(place_index, group));
        population.places()[place_index].addMember(cell->index(), m_cellPos, group);
    }

    void Person::removePlace(Population& population, Cell* cell, size_t place_index, size_t group)
    {
        std::pair<size_t, size_t> r = std::make_pair(place_index, group);
        if (m_places.find(r) == m_places.end()) return;
        m_places.erase(r);
        population.places()[place_index].removeMember(cell->index(), m_cellPos, group);
    }

    void Person::removePlaceAllGroups(Population& population, Cell* cell, size_t place_index)
    {
        for (auto it = m_places.begin(); it != m_places.end();)
        {
            if (it->first != place_index) ++it;
            else m_places.erase(it++);
        }
        population.places()[place_index].removeMemberAllGroups(cell->index(), m_cellPos);
    }

    std::set<std::pair<size_t, size_t>>& Person::places() { return m_places; }

    void Person::forEachPlace(Population& population, std::function<void(Place*, size_t)> callback)
    {
        for (const std::pair<size_t, size_t>& p : m_places)
            callback(&population.places()[p.first], p.second);
    }

} // namespace epiabm


#include "microcell.hpp"
#include "cell.hpp"

namespace epiabm
{

    Microcell::Microcell(size_t cellPos) :
        m_people(),
        m_places(),
        m_households(),
        m_cellPos(cellPos)
    {}

    Microcell::Microcell(const Microcell& other) :
        m_people(other.m_people),
        m_places(other.m_places),
        m_households(other.m_households),
        m_cellPos(other.m_cellPos)
    {}

    Microcell::Microcell(Microcell&& other) :
        m_people(std::move(other.m_people)),
        m_places(std::move(other.m_places)),
        m_households(std::move(other.m_households)),
        m_cellPos(std::move(other.m_cellPos))
    {}

    void Microcell::forEachPerson(Cell& cell, std::function<bool(Person*)> callback)
    {
        for (size_t i = 0; i < m_people.size(); i++)
        {
            if (!callback(&cell.m_people[m_people[i]])) return;
        }
    }

    void Microcell::forEachPlace(std::function<bool(Place*)> callback)
    {
        for (size_t i = 0; i < m_places.size(); i++)
        {
            if (!callback(&m_places[i])) return;
        }
    }

    Person& Microcell::getPerson(Cell& cell, size_t i)
    {
        return cell.m_people[m_people[i]];
    }

} // namespace epiabm

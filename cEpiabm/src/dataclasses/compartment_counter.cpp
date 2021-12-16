
#include "compartment_counter.hpp"
#include "person.hpp"
#include "cell.hpp"

#include <vector>

namespace epiabm
{


    CompartmentCounter::CompartmentCounter() :
        m_counts()
    {}

    void CompartmentCounter::clear()
    {
        m_counts.clear();
    }

    unsigned int CompartmentCounter::operator()(InfectionStatus status) const
    {
        if (m_counts.find(status) != m_counts.end()) return m_counts.at(status);
        else return 0;
    }

    void CompartmentCounter::notify(InfectionStatus old_status, InfectionStatus new_status)
    {
        m_counts[old_status]--;
        m_counts[new_status]++;
    }

    void CompartmentCounter::initialize(Cell* cell, const std::vector<size_t>& people)
    {
        clear();
        for (const auto pi : people)
            m_counts[cell->getPerson(pi).status()]++;
    }

    void CompartmentCounter::initialize(const std::vector<Person>& people)
    {
        clear();
        for (const auto& p : people)
            m_counts[p.status()]++;
    }

}

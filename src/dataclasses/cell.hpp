#ifndef _COVIDSIM_DATACLASSES_CELL_HPP
#define _COVIDSIM_DATACLASSES_CELL_HPP

#include "types.hpp"

#include <boost/function.hpp>

#include <vector>
#include <memory>
#include <functional>
#include <iostream>
#include <queue>

namespace seir
{
    
    class Cell
    {
    private:
        std::vector<PersonPtr> m_people;
        std::vector<MicrocellPtr> m_microcells;

        std::queue<Person*> m_newExposures;

    public:
        Cell();

        void forEachMicrocell(boost::function<bool(MicrocellPtr)> callback);
        void forEachPerson(boost::function<bool(PersonPtr)> callback);

        Person* getPerson(int i) { return m_people[i].get(); }
        Microcell* getMicrocell(int i) { return m_microcells[i].get(); }

        void print() { std::cout << "Cell wih " << m_microcells.size() << " microcells and " << m_people.size() << " people." << std::endl; }
        
        void processNewExposures();
        void addNewExposure(Person* person) { m_newExposures.push(person); }

    private:
        friend class Factory;
    };

} // namespace seir

#endif // _COVIDSIM_DATACLASSES_CELL_HPP
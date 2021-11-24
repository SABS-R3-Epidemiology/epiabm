#ifndef _EPIABM_DATACLASSES_CELL_HPP
#define _EPIABM_DATACLASSES_CELL_HPP

#include "types.hpp"

#include <vector>
#include <memory>
#include <functional>
#include <iostream>
#include <queue>

namespace epiabm
{
    
    class Cell
    {
    private:
        std::vector<PersonPtr> m_people;
        size_t m_numInfected;
        std::vector<MicrocellPtr> m_microcells;

        std::queue<std::weak_ptr<Person>> m_personQueue;

    public:
        Cell();
        ~Cell() = default;

        void forEachMicrocell(std::function<bool(MicrocellPtr)>& callback);
        void forEachPerson(std::function<bool(PersonPtr)>& callback);
        void forEachInfectious(std::function<bool(PersonPtr)>& callback);
        void forEachNonInfectious(std::function<bool(PersonPtr)>& callback);

        PersonPtr getPerson(int i) { return m_people[i]; }
        MicrocellPtr getMicrocell(int i) { return m_microcells[i]; }

        void print() { std::cout << "Cell with " << m_microcells.size() << " microcells and " << m_people.size() << " people." << std::endl; }
        
        void processQueue(std::function<void(PersonPtr)> callback);
        void enqueuePerson(std::weak_ptr<Person> person) { m_personQueue.push(person); }

        std::vector<PersonPtr>& people() { return m_people; }
        std::vector<MicrocellPtr>& microcells() { return m_microcells; }

        void markInfectious(PersonPtr person);
        void markNonInfectious(PersonPtr person);

    private:
        friend class Factory;
    };

} // namespace epiabm

#endif // _EPIABM_DATACLASSES_CELL_HPP
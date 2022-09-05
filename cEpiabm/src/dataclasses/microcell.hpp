#ifndef EPIABM_DATACLASSES_MICROCELL_HPP
#define EPIABM_DATACLASSES_MICROCELL_HPP

#include "person.hpp"
#include "place.hpp"
#include "household.hpp"
#include "compartment_counter.hpp"

#include <vector>
#include <memory>
#include <functional>
#include <exception>
#include <iostream>

namespace epiabm
{
    class Cell;

    class Microcell
    {
    private:
        std::vector<size_t> m_people;
        std::vector<HouseholdPtr> m_households;

        size_t m_cellPos; // index of this microcell in parent cell's m_microcells

        CompartmentCounter m_compartmentCounter;

    public:
        Microcell(size_t cellPos);
        ~Microcell();
        Microcell(const Microcell&);
        Microcell(Microcell&&);

        size_t cellPos() const;

        void forEachPerson(Cell& cell, std::function<bool(Person*)> callback);

        Person& getPerson(Cell& cell, size_t i);
        HouseholdPtr getHousehold(size_t i);

        std::vector<size_t>& people();
        std::vector<HouseholdPtr>& households();

        void initialize(Cell* cell);

        unsigned int compartmentCount(InfectionStatus status);

        void personStatusChange(Person* person, InfectionStatus newStatus, unsigned short timestep);


    private:
        friend class Place;
    };

    typedef std::shared_ptr<Microcell> MicrocellPtr;

} // namespace epiabm

#endif // EPIABM_DATACLASSES_MICROCELL_HPP
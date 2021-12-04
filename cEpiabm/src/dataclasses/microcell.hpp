#ifndef EPIABM_DATACLASSES_MICROCELL_HPP
#define EPIABM_DATACLASSES_MICROCELL_HPP

#include "person.hpp"
#include "place.hpp"
#include "household.hpp"

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
        std::vector<Place> m_places;
        std::vector<Household> m_households;

        size_t m_cellPos;

    public:
        Microcell(size_t cellPos);
        ~Microcell() = default;
        Microcell(const Microcell&);
        Microcell(Microcell&&);

        size_t cellPos() const;

        void forEachPerson(Cell& cell, std::function<bool(Person*)> callback);
        void forEachPlace(std::function<bool(Place*)> callback);

        Person& getPerson(Cell& cell, size_t i);

        void print();

        std::vector<size_t>& people();
        std::vector<Place>& places();
        std::vector<Household>& households();

    private:
        friend class Place;
    };

    typedef std::shared_ptr<Microcell> MicrocellPtr;

} // namespace epiabm

#endif // EPIABM_DATACLASSES_MICROCELL_HPP
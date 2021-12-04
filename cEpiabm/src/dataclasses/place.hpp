#ifndef EPIABM_DATACLASSES_PLACE_HPP
#define EPIABM_DATACLASSES_PLACE_HPP

#include "membersInterface.hpp"

#include <memory>

namespace epiabm
{

    class Cell;
    class Microcell;

    class Place : public MembersInterface
    {
    private:
        size_t m_mcellPos;

    public:
        Place(size_t mcellPos);
        ~Place() {}

        size_t microcellPos() const;

    private:
        friend class PopulationFactory;
    };

    typedef std::shared_ptr<Place> PlacePtr;

} // namespace epiabm

#endif // EPIABM_DATACLASSES_PLACE_HPP

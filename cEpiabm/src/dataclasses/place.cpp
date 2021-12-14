
#include "place.hpp"

namespace epiabm
{

    Place::Place(size_t mcellPos) :
        MembersInterface(mcellPos),
        m_mcellPos(mcellPos)
    {}

    size_t Place::microcellPos() const { return m_mcellPos; }

} // namespace epiabm

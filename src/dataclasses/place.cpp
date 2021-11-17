
#include "place.hpp"

namespace seir
{

    Place::Place(MicrocellPtr microcell) :
        m_microcell(microcell),
        m_members()
    {}

    void Place::forEachMember(boost::function<bool(PersonPtr)> callback)
    {
        auto it = m_members.begin();
        while (it != m_members.end())
        {
            callback(*it);
        }
    }

    bool Place::isMember(PersonPtr person)
    {
        return false;
    }

} // namespace seir

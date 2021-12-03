
#include "place.hpp"

namespace epiabm
{

    Place::Place(size_t mcellPos) :
        m_members(),
        m_mcellPos(mcellPos)
    {}

    void Place::forEachMember(std::function<bool(Person*)>& callback)
    {
        auto it = m_members.begin();
        while (it != m_members.end())
        {
            callback(*it);
        }
    }

    bool Place::isMember(Person*)
    {
        return false;
    }

} // namespace epiabm

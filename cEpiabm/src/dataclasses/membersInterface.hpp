#ifndef EPIABM_DATACLASSES_MEMBERS_INTERFACE_HPP
#define EPIABM_DATACLASSES_MEMBERS_INTERFACE_HPP

#include "person.hpp"

#include <set>
#include <functional>
#include <memory>

namespace epiabm
{
    class Cell;
    class Microcell;

    /**
     * @brief Interface for classes which contain members
     * Can only link people within the same cell
     * NOTE: Initially Household and Place shared this functionality,
     *          but Place has been modified to allow inter-cell linkages.
     *          Interface may not be required anymore since only Households have this functionality
     */
    class MembersInterface
    {
    protected:
        std::set<size_t> m_members; // Indices of people in Microcell::m_people vector

    public:
        /**
         * @brief Construct a new Members Interface object
         * 
         */
        MembersInterface();
        virtual ~MembersInterface() = default;

        /**
         * @brief Loop through each member
         * 
         * @param cell 
         * @param microcell 
         * @param callback 
         */
        virtual void forEachMember(Cell &cell, Microcell &microcell,
            std::function<bool(Person *)> callback);
        virtual bool isMember(size_t person) const;

        virtual bool addMember(size_t person); // Maybe should make this private

        virtual std::set<size_t> &members();

    private:
    };

    typedef std::shared_ptr<MembersInterface> MembersInterfacePtr;

} // epiabm

#endif // EPIABM_DATACLASSES_MEMBERS_INTERFACE_HPP
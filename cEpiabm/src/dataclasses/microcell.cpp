
#include "cell.hpp"
#include "microcell.hpp"

namespace epiabm
{

    /**
     * @brief Construct a new Microcell:: Microcell object
     * 
     * @param cellPos Microcell's index within parent cell
     */
    Microcell::Microcell(size_t cellPos) :
        m_people(),
        m_households(),
        m_cellPos(cellPos),
        m_compartmentCounter()
    {}

    /**
     * @brief Destroy the Microcell:: Microcell object
     * 
     */
    Microcell::~Microcell()
    {
        //std::cout << "Microcell Destructor" << std::endl;
    }

    Microcell::Microcell(const Microcell& other) :
        m_people(other.m_people),
        m_households(other.m_households),
        m_cellPos(other.m_cellPos)
    {}

    Microcell::Microcell(Microcell&& other) :
        m_people(std::move(other.m_people)),
        m_households(std::move(other.m_households)),
        m_cellPos(std::move(other.m_cellPos))
    {}

    /**
     * @brief Get index of microcell in parent cell
     * 
     * @return size_t Microcell's index within parent cell's microcells vector
     */
    size_t Microcell::cellPos() const { return m_cellPos; }

    /**
     * @brief Apply callback to each person in microcell
     * 
     * Callback can return false to terminate loop early
     * 
     * @param cell Reference to microcell's parent cell
     * @param callback Callback to apply to each person in microcell
     */
    void Microcell::forEachPerson(Cell& cell, std::function<bool(Person*)> callback)
    {
        for (size_t i = 0; i < m_people.size(); i++)
        {
            if (!callback(&cell.m_people[m_people[i]])) return;
        }
    }

    /**
     * @brief Get person in microcell
     * 
     * @param cell Reference to microcell's parent cell
     * @param i Index within microcell's people vector to retrieve
     * @return Person& Reference to ith person in microcell's people vector
     */
    Person& Microcell::getPerson(Cell& cell, size_t i)
    {
        return cell.m_people[m_people[i]];
    }

    /**
     * @brief Get ith houshold in microcell
     * 
     * @param i Index of household to retrieve
     * @return HouseholdPtr Shared pointer to ith household in microcell
     */
    HouseholdPtr Microcell::getHousehold(size_t i)
    {
        return m_households[i];
    }

    /**
     * @brief Get reference to microcell's people vector
     * 
     * Each entry in vector corresponds to index of person in parent cell's vector.
     * 
     * @return std::vector<size_t>& Reference to microcell's people vector
     */
    std::vector<size_t>& Microcell::people() { return m_people; }
    /**
     * @brief Get reference to microcell's households vector
     * 
     * @return std::vector<HouseholdPtr>& Reference to microcell's households vector
     */
    std::vector<HouseholdPtr>& Microcell::households() { return m_households; }

    /**
     * @brief Initialize Microcell
     * 
     * Automatically called by parent cell during Population::initialize().
     * Part of population's pre-simulation initialization procedure
     * 
     * @param cell Pointer to parent cell
     */
    void Microcell::initialize(Cell* cell)
    {
        m_compartmentCounter.initialize(cell, m_people);
    }

    /**
     * @brief Retrieve number of people with specific InfectionStatus
     * 
     * @param status Compartment to retrieve
     * @return unsigned int Number of people in the compartment
     */
    unsigned int Microcell::compartmentCount(InfectionStatus status)
    {
        return m_compartmentCounter(status);
    }

    /**
     * @brief Change a person's status
     * 
     * Automatically called during Person::updateStatus by parent Cell::updateStatus.
     * Should not be called manually
     * Part of person update status procedure
     * 
     * @param person Person to alter
     * @param newStatus Person's new status
     * @param timestep Time of status change
     */
    void Microcell::personStatusChange(Person* person, InfectionStatus newStatus, unsigned short /*timestep*/)
    {
        m_compartmentCounter.notify(person->status(), newStatus);
    }

} // namespace epiabm

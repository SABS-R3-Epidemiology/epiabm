#include "random_manager.hpp"


namespace epiabm
{

    RandomManager::RandomManager(unsigned int seed) :
        m_generators(),
        m_seed(seed)
    {}

    RandomManager::~RandomManager() = default;

    RandomGenerator& RandomManager::g()
    {
        std::thread::id tid = std::this_thread::get_id();
        if (m_generators.find(tid) == m_generators.end())
            m_generators[tid] = std::make_shared<RandomGenerator>(
                m_seed + m_nThreads, m_nThreads, tid);
        return *m_generators.at(tid);
    }

}
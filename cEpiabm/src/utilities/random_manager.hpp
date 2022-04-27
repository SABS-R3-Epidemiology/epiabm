#ifndef EPIABM_UTILITIES_RANDOM_MANAGER_HPP
#define EPIABM_UTILITIES_RANDOM_MANAGER_HPP


#include "random_generator.hpp"

#include <map>
#include <thread>
#include <memory>


namespace epiabm
{

    class RandomManager
    {
    private:
        std::map<std::thread::id, RandomGeneratorPtr> m_generators;
        unsigned int m_nThreads;
        unsigned int m_seed;

    public:
        RandomManager(unsigned int seed);
        ~RandomManager();

        RandomGenerator& g();

    private:
    };

    typedef std::shared_ptr<RandomManager> RandomManagerPtr;

} // namespace epiabm


#endif // EPIABM_UTILITIES_RANDOM_MANAGER_HPP
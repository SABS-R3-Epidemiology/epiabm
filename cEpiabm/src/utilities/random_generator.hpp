#ifndef EPIABM_UTILITIES_RANDOM_GENERATOR_HPP
#define EPIABM_UTILITIES_RANDOM_GENERATOR_HPP


#include <map>
#include <thread>
#include <random>
#include <mutex>
#include <memory>
#include <iostream>
#include <limits>

namespace epiabm
{

    class RandomGenerator
    {
    private:
        size_t m_threadNum;
        std::thread::id m_threadId;

        unsigned int m_seed;
        unsigned long long int m_counter;
        std::mt19937_64 m_generator;

        std::mutex m_mutex;

    public:
        RandomGenerator(unsigned int seed, size_t threadNum) :
            m_threadNum(threadNum),
            m_seed(seed),
            m_counter(0)
        {
            m_threadId = std::this_thread::get_id();
            m_generator = std::mt19937_64(seed);
        }

        RandomGenerator(unsigned int seed, size_t threadNum, std::thread::id threadId) :
            m_threadNum(threadNum),
            m_threadId(threadId),
            m_seed(seed)
        {
            m_generator = std::mt19937_64(seed);
        }

        ~RandomGenerator() = default;

        std::mt19937_64& generator() { return m_generator; }
        
        /**
         * @brief Generate Random Integer
         * Random integer between 0 and max inclusive
         * 
         * @tparam T Integer Type
         * @param max 
         * @return T Generated Random Number
         */
        template <typename T>
        T randi(T max)
        {
            std::lock_guard<std::mutex> lock = std::lock_guard(m_mutex);
            ++m_counter;
            return static_cast<T>(m_generator() % std::numeric_limits<T>::max()) % (max + 1);
        }

        /**
         * @brief Generate Random Integer Type
         * Random integer between min and max inclusive
         * 
         * @tparam T Integer Type
         * @param min 
         * @param max 
         * @return T Generated Random Number
         */
        template <typename T>
        T randi(T min, T max)
        {
            std::lock_guard<std::mutex> lock = std::lock_guard(m_mutex);
            ++m_counter;
            return static_cast<T>(min + static_cast<T>(m_generator() % std::numeric_limits<T>::max()) % (max - min + 1));
        }

        /**
         * @brief Generate Random Floating Point Type
         * 
         * @tparam T Float Type
         * @return T Generated Float Type
         */
        template <typename T>
        T randf()
        {
            std::lock_guard<std::mutex> lock = std::lock_guard(m_mutex);
            return static_cast<T>(m_generator()) / static_cast<T>(m_generator.max());
        }


    private:
    };

    typedef std::shared_ptr<RandomGenerator> RandomGeneratorPtr;

    template int RandomGenerator::randi<int>(int max);
    template long RandomGenerator::randi<long>(long max);
    template unsigned int RandomGenerator::randi<unsigned int>(unsigned int max);
    template unsigned long RandomGenerator::randi<unsigned long>(unsigned long max);

    template int RandomGenerator::randi<int>(int min, int max);
    template long RandomGenerator::randi<long>(long min, long max);
    template unsigned int RandomGenerator::randi<unsigned int>(unsigned int min, unsigned int max);
    template unsigned long RandomGenerator::randi<unsigned long>(unsigned long min, unsigned long max);

    template float RandomGenerator::randf<float>();
    template double RandomGenerator::randf<double>();

} // namespace epiabm

#endif // EPIABM_UTILITIES_RANDOM_GENERATOR_HPP

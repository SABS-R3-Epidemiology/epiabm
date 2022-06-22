#ifndef EPIABM_TEST_CONFIGURATION_HELPERS_HPP
#define EPIABM_TEST_CONFIGURATION_HELPERS_HPP

#include "utilities/inverse_cdf.hpp"

#include <random>

#include "../catch/catch.hpp"

namespace detail
{
    const char alphanum[] =
        "0123456789"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz";

    template <typename T>
    inline T generate()
    {
        return static_cast<T>(std::rand());
    }

    inline std::string generate(size_t n = 10)
    {
        std::string s;
        s.reserve(n);
        for (size_t i = 0; i < n; i++)
        {
            s += alphanum[static_cast<size_t>(std::rand()) % (sizeof(alphanum)-1)];
        }
        return s;
    }

}


template <typename T>
inline void checkParameter(T& var, size_t reps = 1)
{
    for (size_t r = 0; r < reps; r++)
    {
        const T value = detail::generate<T>();
        var = value;
        REQUIRE(var == value);
    }
}

template <typename T, size_t N>
inline void checkParameter(std::array<T, N>& var, size_t reps = 1)
{
    for (size_t r = 0; r < reps; r++)
    {
        std::array<T, N> value;
        for (size_t i = 0; i < N; i++)
        {
            value[i] = detail::generate<T>();
            var[i] = value[i];
        }

        for (size_t i = 0; i < N; i++)
        {
            REQUIRE(var[i] == value[i]);
        }
    }
}

template <>
inline void checkParameter<epiabm::InverseCDF>(epiabm::InverseCDF& var, size_t reps)
{
    checkParameter(var.getValues(), reps);
}

#endif // EPIABM_TEST_CONFIGURATION_HELPERS_HPP

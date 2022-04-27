#ifndef EPIABM_UTILITIES_INVERSE_CDF_HPP
#define EPIABM_UTILITIES_INVERSE_CDF_HPP

#include <array>
#include <random>

namespace epiabm
{
    class InverseCDF
    {
    public:
        static const size_t RES = 20;
    private:
        std::array<double, InverseCDF::RES + 1> m_values;
        double m_mean;

    public:
        InverseCDF();
        InverseCDF(double mean);

        void setNegLog(double startValue);
        void assignExponent();
        void assignExponent(double value);

        unsigned short choose(double timestepsPerDay, std::mt19937_64 generator);

        std::array<double, InverseCDF::RES+1>& getValues();
        double& operator[](size_t i);

    private:
    };

} // namespace epiabm

#endif // EPIABM_UTILITIES_INVERSE_CDF_HPP

#ifndef EPIABM_UTILITY_DISTANCE_METRICS_HPP
#define EPIABM_UTILITY_DISTANCE_METRICS_HPP


#include <vector>


namespace epiabm
{
    typedef std::pair<double, double> location;

    class DistanceMetrics
    {
        public:
            DistanceMetrics();
            ~DistanceMetrics() = default;

            static double Dist(location loc1, location loc2);
            static double DistEuclid(location loc1, location loc2);
            static double DistCovidsim(location loc1, location loc2);
    };
} // namespace epiabm

#endif // EPIABM_UTILITY_DISTANCE_METRICS_HPP
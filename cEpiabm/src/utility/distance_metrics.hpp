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

            static double dist(location loc1, location loc2);
            static double distEuclid(location loc1, location loc2);
            static double distCovidsim(location loc1, location loc2);
    };
} // namespace epiabm

#endif // EPIABM_UTILITY_DISTANCE_METRICS_HPP
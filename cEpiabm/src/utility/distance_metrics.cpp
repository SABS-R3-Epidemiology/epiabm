#include "distance_metrics.hpp"
#include <cmath>


namespace epiabm
{


    DistanceMetrics::DistanceMetrics()
    {}

    double DistanceMetrics::Dist(location loc1, location loc2)
    { 
        return DistEuclid(loc1, loc2);
    }
            
    double DistanceMetrics::DistEuclid(location loc1, location loc2)
    {
        return pow(loc1.first-loc2.first, 2) + pow(loc1.second-loc2.second, 2);
    }
            
    double DistanceMetrics::DistCovidsim(location /*loc1*/, location /*loc2*/)
    {
        return 2;
    }

} // namespace epiabm


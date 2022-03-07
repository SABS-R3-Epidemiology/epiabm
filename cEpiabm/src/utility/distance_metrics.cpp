#include "distance_metrics.hpp"
#include <cmath>


namespace epiabm
{


    DistanceMetrics::DistanceMetrics()
    {}

    double dist(location loc1, location loc2)
    { 
        return distEuclid(loc1, loc2);
    }
            
    double distEuclid(location loc1, location loc2)
    {
        return pow(loc1.first-loc2.first, 2) + pow(loc1.second-loc2.second, 2);
    }
            
    double distCovidsim(location loc1, location loc2)
    {
        return 2;
    }

} // namespace epiabm


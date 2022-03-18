#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "utilities/inverse_cdf.hpp"

namespace py = pybind11;

void bind_utilities(py::module &m)
{
    using namespace epiabm;

    py::class_<InverseCDF>(m, "InverseCDF")
        .def(py::init<double>())
        .def("choose", &InverseCDF::choose, "Generate random number from iCDF")
        .def("values", &InverseCDF::getValues, "Get iCDF values",
            py::return_value_policy::reference);

}


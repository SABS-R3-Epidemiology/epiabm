#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "utilities/inverse_cdf.hpp"
#include "utilities/random_generator.hpp"
#include "utilities/random_manager.hpp"

namespace py = pybind11;

void bind_utilities(py::module &m)
{
    using namespace epiabm;

    py::class_<InverseCDF>(m, "InverseCDF")
        .def(py::init<double>())
        .def("choose", &InverseCDF::choose, "Generate random number from iCDF",
            py::arg("timesteps_per_day")=1, py::arg("generator"))
        .def("values", &InverseCDF::getValues, "Get iCDF values",
            py::return_value_policy::reference)
        .def("mean", &InverseCDF::mean, "Get iCDF mean",
            py::return_value_policy::copy);

    py::class_<RandomManager, RandomManagerPtr>(m, "RandomManager")
        .def("generator", &RandomManager::g, "Get RandomGenerator",
            py::return_value_policy::reference);

    py::class_<RandomGenerator, RandomGeneratorPtr>(m, "RandomGenerator")
        .def("randi", py::overload_cast<long, long>(&RandomGenerator::randi<long>), "Generate Random Long",
            py::return_value_policy::copy)
        .def("randf", &RandomGenerator::randf<double>, "Generate Random Double",
            py::return_value_policy::copy)
        .def("generator", &RandomGenerator::generator, "Underlying mersenne twister generator",
            py::return_value_policy::reference);

}


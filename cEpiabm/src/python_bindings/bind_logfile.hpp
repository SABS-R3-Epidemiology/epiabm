#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <pybind11/stl/filesystem.h>

#include "logfile.hpp"


namespace py = pybind11;

void bind_logfile(py::module &m)
{
    using namespace epiabm;

    py::class_<LogFile>(m, "LogFile")
        .def_static("Instance", &LogFile::Instance, py::return_value_policy::reference)
        .def("configure", &LogFile::configure)
        .def("set_level", &LogFile::setLevel);
}


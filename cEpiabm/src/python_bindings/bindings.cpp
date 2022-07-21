#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "bind_dataclasses.hpp"
#include "bind_sweeps.hpp"
#include "bind_reporters.hpp"
#include "bind_simulation.hpp"
#include "bind_logfile.hpp"

namespace py = pybind11;

PYBIND11_MODULE(epiabm, m)
{
    using namespace epiabm;
    bind_dataclasses(m);
    bind_sweeps(m);
    bind_reporters(m);
    bind_simulation(m);
    bind_logfile(m);
}


cEpiabm
=======

We provide an efficient and scalable backend in C++, which can run
simulations for populations comparable to the UK in a reasonable
timeframe. This code may be harder than pyEpiabm for new users to
understand, but the parallels with the python code should be
sufficiently informative for those who wish to look deeper into the
code.

Set up
------

Installation of cEpiabm
~~~~~~~~~~~~~~~~~~~~~~~

Cmake is used for installation of the cEpiabm software. The following
procedure will compile the code and run all unit tests:

.. code:: console

   mkdir build_dir
   cd build_dir
   cmake ../cEpiabm/. -DCMAKE_BUILD_TYPE=Debug
   cmake --build . --parallel 2 --target unit_tests
   ctest -j2 --output-on-failure

Note that cmake must be installed on your system. The following command
can be used on ubuntu systems:

.. code:: console

   sudo apt-get install cmake cmake-data

Compiling cEpiabm Python Bindings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pybind11 is required for compiling cEpiabm with Python bindings.
Pybind11 is added as a git submodule, make sure this submodule is cloned
along with the main epiabm repository.

Compiling Python bindings follows similar procedure to compiling the
cEpiabm tests:

.. code:: console

   mkdir build_dir
   cd build_dir
   cmake ../cEpiabm/. -DCMAKE_BUILD_TYPE=Release -DENABLE_COVERAGE=OFF
   cmake --build . --parallel 6 --target epiabm

cEpiabm’s python bindings will be compiled to a python module named
epiabm, located in ``build_dir/src/epiabm.cpython-(version info).so``.

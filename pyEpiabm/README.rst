pyEpiabm
========

The pyEpiabm backend is written in python, chosen for its readability
and user-friendliness. It is not able to cope with large population
sizes, but can configure a toy population to explore the functionality
of the model and better understand the underlying code. Additionally,
toy models may be quicker for model comparison and parameter inference,
though care should obviously be taken when scaling up to a full
population. We provide a variety of workflows to show the utility of
code.

Installation of pyEpiabm
------------------------

pyEpiabm is not yet available on `PyPI <https://pypi.org/>`__, but the
module can be pip installed locally. The directory should first be
downloaded to your local machine, and can then be installed using the
command:

.. code:: console

   pip install -e .

from the ``pyEpiabm`` directory. If you also wish to build the docs
locally, this requires additional dependencies, which must be specified:

.. code:: console

   pip install -e .[docs]

Running a simulation
--------------------

A number of example simulations are included the in the
``python_examples`` directory. The simplest complete workflow for
running a simulation is provided in
``python_examples/basic_example/simulation_flow.py``, but all others
follow a similar format. Other example simulations include an
``age_stratified_example``, and ``spatial_example`` which demonstrate
these aspects of the module. ``gilbraltar_example`` combines age and
spatial stratification using census data from Gibraltar, and can be used
to benchmark against CovidSIM.

There are a number of steps to any simulation:

Set Random Seed *(Optional)*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This allows the random seed to be set for all random modules used in the
simulation, to enable reproducible simulations. The recommended approach
here is to set one seed at the start of the script (before configuring
the population or the simulation objects), so that both are generated
according to this seed. It is also possible to set a separate seed for
one or other object, by passing ``population_seed`` or
``simulation_seed`` into their respective parameter dictionaries,
however care should be exercised to ensure the two objects are
configured sequentially. For example, generating a second population
after setting the simulation seed would be done according to
``simulation_seed`` not ``population_seed``. Setting the seed is not
currently compatible with multi-threaded execution.

Configure Population
~~~~~~~~~~~~~~~~~~~~

Create a population based on the parameters given, from the following
list:

-  ``population_size``: Number of people in population
-  ``cell_number``: Number of cells in population
-  ``microcell_number``: Number of microcells in each cell
-  ``household_number``: Number of households in each microcell
   *(Optional)*
-  ``place_number``: Number of places in each microcell *(Optional)*
-  ``population_seed``: Random seed for reproducible populations - see
   above *(Optional)*

Import Population
~~~~~~~~~~~~~~~~~

Alternatively, it is possible to import a population from a ``.csv``
file, with the following headings:

-  ``cell``: ID code for cell
-  ``microcell``: ID code for microcell
-  ``location_x``: The x coordinate of the parent cell location
-  ``location_y``: The y coordinate of the parent cell location
-  ``household_number``: Number of households in that microcell
-  Any number of columns with titles from the ``InfectionStatus`` enum
   (such as ``InfectionStatus.Susceptible``), giving the number of
   people with that status in that cell

File of this format can also be exported using the
``pyEpiabm.routine.FilePopulationConfig.print_population()`` method,
i.e. for reproducibility or use in further simulations.

Configure Simulation
~~~~~~~~~~~~~~~~~~~~

Configure a simulation with a number of parameters. These are split into
three categories:

sim_params
""""""""""

- ``simulation_start_time``: The initial time at the start of the simulation
- ``simulation_end_time``: The final time at which to stop the simulation
- ``initial_infected_number``: The initial number of infected individuals in the population
- ``initial_infect_cell``: Whether to choose initial infected individuals from a single cell
- ``simulation_seed``: Random seed for reproducible simulations - see above *(Optional)*
- ``include_waning``: Boolean to determine whether immunity waning is included in the simulation *(Default false)*

file_params
"""""""""""
*(For controlling output location)*

- ``output_file``: String for the name of the output .csv file
- ``output_dir``: String for the location of the output file, as a relative path
- ``spatial_output``: Boolean to determine whether a spatial output should be used *(Default false)*
- ``age_stratified``: Boolean to determine whether the output will be age stratified *(Default false)*

inf_history_params
""""""""""""""""""
*(For controlling the infection history output - Default None)*

- ``output_dir``: String for the location for the output files, as a relative path
- ``status_output``: Boolean to determine whether we need a csv file containing infection status values *(Default false)*
- ``infectiousness_output``: Boolean to determine whether we need a csv file containing infectiousness (viral load) values *(Default false)*
- ``compress``: Boolean to determine whether we compress a csv file containing infection status values and/or a csv file containing infectiousness (viral load) values if they are written *(Default false)*

Two lists of sweeps must also be passed to this function - the first
will be executed once at the start of the simulation (i.e. to determine
the initial infections in the population), while the second list will be
ran at every timestep (i.e. to propagate the infection through the
population).

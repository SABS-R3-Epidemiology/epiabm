## Northern Ireland Example

In the `NI_example` directory, the `NI_flow.py` script simulates the spread of a COVID-like disease across Northern Ireland, which has a population just shy of 2 million. This simulation demonstrates the breadth of data our agent-based model can generate. Five key files (too large to be uploaded) are produced from this simulation, along with the standard `output.csv`: `demographics.csv`, `inf_status_history.csv`, `secondary_infections.csv`, `serial_intervals.csv` and `generation_times.csv`. In the demographics file, we record the ID, age, home location and care home status of each individual at the beginning of the simulation. Each timestep, we then record the infection status of every person (keyed by their ID) in `inf_status_history.csv`. We also record the total number of secondary infections each primary infector causes in `secondary_infections.csv`; this is used to calculate the time-varying reproduction number of the simulation. Finally, we also record each serial interval (time between symptom onset of a primary and secondary case) and generation time (time between exposure to disease of a primary and secondary case), which can be used to generate histograms for these quantities. As a caveat, we also record the serial interval for asymptomatic cases and define their "symptom onset" as the timepoint in which they have infection status I.

To run this simulation, first clone the repository and `cd` into the correct directory:

```
git clone git@github.com:SABS-R3-Epidemiology/epiabm.git
cd epiabm
python3 -m venv venv
source venv/bin/activate
pip install -e pyEpiabm/
cd python_examples/NI_example
```

From here, if you wish to update any simulation parameters, you have two options. To edit parameters such as the run time, initial infected population, which output files to produce and the waning immunity flag, simply enter the flow file and make the desired changes.

```
nano NI_flow.py
```

Geospatial and epidemic-specific parameters are in the .json file. Here, the infection_radius can be edited, which controls the maximum distance in which an infected individual can travel across the country. We advise that other parameters are left untouched, as these are from CovidSim, census data and other literature (see the [Wiki](https://github.com/SABS-R3-Epidemiology/epiabm/wiki) for more information).

Once parameters have been edited, simply run the file

```
python NI_flow.py
```

Due to the large population size, this simulation requires a large amount of memory and takes a long time to run. We ran these simulations using a CPU compute system with 1536 GB RAM and a speed of 2.6–3.9 GHz.

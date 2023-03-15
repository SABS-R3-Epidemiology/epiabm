import os
import sys
import logging
import pandas as pd
import matplotlib.pyplot as plt

# Add plotting functions to path
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir,
                "./age_stratified_example"))
from age_stratified_plot import Plotter  # noqa

# Setup output for logging file
logging.basicConfig(filename='sim.log', filemode='w+', level=logging.DEBUG,
                    format=('%(asctime)s - %(name)s'
                            + '- %(levelname)s - %(message)s'))

# Creation of a plot of results (plotter from spatial_simulation_flow)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
filename = os.path.join(os.path.dirname(__file__),
                        "simulation_outputs/large_csv/",
                        "output_new_brunswick.csv")
print('Marker 1')
SIRdf = pd.read_csv(filename)
print('Marker 2')
total = SIRdf[list(SIRdf.filter(regex='InfectionStatus.Infect'))]
SIRdf["Infected"] = total.sum(axis=1)
SIRdf = SIRdf.groupby(["time"]).agg(
                                {"InfectionStatus.Susceptible": 'sum',
                                 "Infected": 'sum',
                                 "InfectionStatus.Recovered": 'sum',
                                 "InfectionStatus.Dead": 'sum'})
SIRdf.rename(columns={"InfectionStatus.Susceptible": "Susceptible",
                      "InfectionStatus.Recovered": "Recovered"},
             inplace=True)
# Create plot to show SIR curves against time
SIRdf.plot(y=["Susceptible", "Infected", "Recovered"])
plt.savefig(os.path.join(os.path.dirname(__file__),
            "simulation_outputs/NB_simulation_flow_SIR_plot.png"))

# Creation of a plot of results with age stratification
# if file_params["age_stratified"]:
p = Plotter(os.path.join(os.path.dirname(__file__),
            "simulation_outputs/large_csv/output_new_brunswick.csv"),
            start_date='18-03-2022', sum_weekly=True)
p.barchart(os.path.join(os.path.dirname(__file__),
           "simulation_outputs/age_stratify_new_brunswick.png"),
           write_Df_toFile=os.path.join(os.path.dirname(__file__),
           "simulation_outputs/new_brunswick_weeky_cases.csv"),
           param_file=os.path.join(os.path.dirname(__file__),
           "canada_parameters.json"))

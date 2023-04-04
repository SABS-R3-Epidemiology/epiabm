import os
import sys
import logging
import pandas as pd
import matplotlib.pyplot as plt

# Add plotting functions to path
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir,
                "./age_stratified_example"))
from age_stratified_plot import Plotter  # noqa

# Creation of a plot of results (plotter from spatial_simulation_flow)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
filename = os.path.join(os.path.dirname(__file__),
                        "simulation_outputs/large_csv",
                        "output_0.375.csv")
SIRdf = pd.read_csv(filename)
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
            "simulation_outputs/simulation_flow_SIR_plot.png"))

p = Plotter(os.path.join(os.path.dirname(__file__),
            "simulation_outputs/large_csv/output_0.375.csv"),
            start_date='29-02-2020', sum_weekly=True)
p.barchart(os.path.join(os.path.dirname(__file__),
           "simulation_outputs/age_stratify.png"),
           write_Df_toFile=os.path.join(os.path.dirname(__file__),
           "simulation_outputs/luxembourg_weeky_cases.csv"),
           param_file=os.path.join(os.path.dirname(__file__),
           "luxembourg_parameters.json"))

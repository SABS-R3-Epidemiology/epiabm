import os
import sys

# Add plotting functions to path
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir,
                "./age_stratified_example"))
from age_stratified_plot import Plotter  # noqa

# Creation of a plot of results with age stratification
# if file_params["age_stratified"]:
p = Plotter(os.path.join(os.path.dirname(__file__),
            "simulation_outputs/large_csv/output_winnipeg.csv"),
            start_date='18-03-2022', sum_weekly=True)
p.barchart(os.path.join(os.path.dirname(__file__),
           "simulation_outputs/winnipeg_age_stratify.png"),
           write_Df_toFile=os.path.join(os.path.dirname(__file__),
           "simulation_outputs/winnipeg_weeky_cases.csv"),
           param_file=os.path.join(os.path.dirname(__file__),
           "canada_parameters.json"))

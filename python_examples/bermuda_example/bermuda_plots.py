import os
import sys
import logging
import pandas as pd
import matplotlib.pyplot as plt

import pyEpiabm as pe

# Add plotting functions to path
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir,
                "./age_stratified_example"))
from age_stratified_plot import Plotter  # noqa

# Creation of a plot of results with age stratification
# if file_params["age_stratified"]:
p = Plotter(os.path.join(os.path.dirname(__file__),
            "simulation_outputs/output_bermuda.csv"),
            start_date='18-03-2022', sum_weekly=True)
p.barchart(os.path.join(os.path.dirname(__file__),
           "simulation_outputs/age_stratify.png"),
           write_Df_toFile=os.path.join(os.path.dirname(__file__),
           "simulation_outputs/bermuda_weeky_cases.csv"),
           param_file=os.path.join(os.path.dirname(__file__),
           "bermuda_parameters.json"))
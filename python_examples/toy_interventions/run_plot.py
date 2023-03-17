import pyEpiabm as pe

from toy_plotter import Plotter 

# Creation of a plot of results with age stratification
p = Plotter('simulation_outputs', [4, 15], 5, 10, 'isolation_probability', [0.0, 1.0])
p._summarise_outputs()
p._multiple_curve_plotter('test3')
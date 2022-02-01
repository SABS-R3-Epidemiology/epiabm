# Python Examples

This directory contains a number of examples of python workflows to run simulations with pEpiabm. New users are suggested to use the `simulation_flow.py` script to run a basic simulation with little initial configuration. More complex examples are given in subdirectories of this folder.

## Simulation Flow

This script outlines all commands necessary to run a basic simulation. It models a population of 100 individuals, spread across 20 households in a single cell and microcell.

It subsequently saves the results to a .csv file, and plots a basic SIR plot of the simulation output, depicted below:

![SIR plot from simulation_flow.pt](./simulation_outputs/simulation_flow_SIR_plot.png)

## Spatial Simulations 

Contained within the `spatial_example/` directory, this script runs a basic simulation with spatial dependance. It considers a population of 1000 individuals, spread across 40 households in 20 cells, each with a single microcell.

It subsequently saves the results to a .csv file, and plots the infection curve for each region. There is currently no differentiation between cells, and so any variation is due to random fluctuations. Any null curves are because there were no infectious individuals seeded in that cell, and no inter-cellular infection mechanisms are currently implemented.

![Infection curves for multiple cells.pt](./spatial_example/spatial_outputs/spatial_flow_Icurve_plot.png)
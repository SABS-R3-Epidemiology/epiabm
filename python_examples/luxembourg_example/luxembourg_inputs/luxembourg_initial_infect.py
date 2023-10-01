# Script to infect an initial number of people in a specific cell
# Outputs a csv file in the format required by pyEpiabm as an input

import pandas as pd
import random

input = pd.read_csv('luxembourg_input_file.csv')
listofzeros = [0] * len(input['location_x'])
cell_number = 1664
initial_infect = 5
index_list = input.index[(input['cell'] == cell_number) & (input['Susceptible']
                         != 0)].tolist()
for i in range(initial_infect):
    index = random.choice(index_list)
    listofzeros[index] += 1
input['InfectMild'] = listofzeros
input.to_csv('luxembourg_adapted_5_in_cell_input.csv', index=False)

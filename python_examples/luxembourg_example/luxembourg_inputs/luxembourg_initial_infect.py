import pandas as pd
import random

input = pd.read_csv('luxembourg_input_file.csv')
listofzeros = [0] * len(input['location_x'])
cell_number = 1664
index_list = input.index[(input['cell'] == cell_number) & (input['Susceptible']
                         != 0)].tolist()
# for i in range(5):
index = random.choice(index_list)
listofzeros[index] += 1
input['InfectMild'] = listofzeros
input.to_csv('luxembourg_adapted_input.csv', index=False)

import os
import pandas as pd
import matplotlib.pyplot as plt

file_name = "simulation_outputs/new_average/combined_summary.csv"
average_output = "simulation_outputs/new_average/combined_av.png"

combined_df = pd.read_csv(file_name)
plt.figure()

grid_list = [4, 6, 8, 12, 15]
colour_list = ['b-', 'g-', 'r-', 'k-', 'c-']
band_list = ['b', 'g', 'r', 'k', 'c']

count = 0
for element in grid_list:
    y_lower = []
    y_upper = []

    for e in range(len(combined_df['sd_infections_{}'.format(element)])):
        value = combined_df['av_infections_{}'.format(element)][e]
        sd = combined_df['sd_infections_{}'.format(element)][e]
        y_lower.append(value-sd)
        y_upper.append(value+sd)

    plt.plot(combined_df['time'], combined_df['av_infections_{}'.format(element)], colour_list[count], label=(str(element)+'x'+str(element)))
    plt.legend()
    plt.fill_between(combined_df['time'], 
                     combined_df['av_infections_{}'.format(element)] - combined_df['sd_infections_{}'.format(element)], 
                     combined_df['av_infections_{}'.format(element)] + combined_df['sd_infections_{}'.format(element)], 
                     color=band_list[count], alpha=0.2)

    count += 1

plt.savefig(os.path.join(os.path.dirname(__file__),
            average_output))


#def generate_data(df, )
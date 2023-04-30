import os
import pandas as pd
import matplotlib.pyplot as plt

r0 = [1.2, 1.5, 2]
for r in r0:
    file_name = "simulation_outputs/change_r0/combined_summary_r0{}.csv".format(r)
    average_output = "simulation_outputs/change_r0/combined_innf_r0{}.png".format(r)

    combined_df = pd.read_csv(file_name)
    plt.figure()

    grid_list = [4, 6, 8, 12, 15]
    colour_list = ['b-', 'g-', 'r-', 'k-', 'c-']
    band_list = ['b', 'g', 'r', 'k', 'c']

    count = 0
    for element in grid_list:

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

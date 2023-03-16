import os
import pandas as pd
import matplotlib.pyplot as plt

file_name = "summary_4x4_av5.csv"
average_output = "simulation_outputs/4x4_av5_places_av.png"

combined_df = pd.read_csv(file_name)

y_lower = []
y_upper = []

for e in range(len(combined_df['sd_infections'])):
    value = combined_df['av_infections'][e]
    sd = combined_df['sd_infections'][e]
    y_lower.append(value-sd)
    y_upper.append(value+sd)

plt.figure()
plt.plot(combined_df['time'], combined_df['av_infections'], 'b-', label='Average')
plt.fill_between(combined_df['time'], combined_df['av_infections'] - combined_df['sd_infections'], combined_df['av_infections'] + combined_df['sd_infections'], color='b', alpha=0.2)

plt.savefig(os.path.join(os.path.dirname(__file__),
            average_output))

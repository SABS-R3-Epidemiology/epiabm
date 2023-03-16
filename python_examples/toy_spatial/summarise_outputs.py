import os
import pandas as pd
import matplotlib.pyplot as plt

file_names = ["output_4x4_av5_0.csv", "output_4x4_av5_1.csv", "output_4x4_av5_2.csv", "output_4x4_av5_3.csv", "output_4x4_av5_4.csv", "output_4x4_av5_5.csv",
              "output_4x4_av5_4.csv", "output_4x4_av5_7.csv", "output_4x4_av5_4.csv", "output_4x4_av5_9.csv"]
output_name = "summary_4x4_av5.csv"
infection_curve_output = "simulation_outputs/4x4_av5_places_plot_infections.png"
size = 4

combined_df = pd.DataFrame()
summary_df = pd.DataFrame()

count = 0
for file in file_names:
    filename = os.path.join(os.path.dirname(__file__), "simulation_outputs",
                            file)
    SIRdf = pd.read_csv(filename)
    total = SIRdf[list(SIRdf.filter(regex='InfectionStatus.Infect'))]
    SIRdf["Infected"] = total.sum(axis=1)
    SIRdf = SIRdf.groupby(["time"]).agg(
                                    {"InfectionStatus.Susceptible": 'sum',
                                     "Infected": 'sum',
                                     "InfectionStatus.Recovered": 'sum',
                                     "InfectionStatus.Dead": 'sum'})
    SIRdf.rename(columns={"InfectionStatus.Susceptible": "Susceptible_{}".format(count),
                          "InfectionStatus.Recovered": "Recovered_{}".format(count),
                          "Infected": "Infected_{}".format(count)},
                 inplace=True)
    combined_df["Susceptible_{}".format(count)] = SIRdf["Susceptible_{}".format(count)]
    combined_df["Recovered_{}".format(count)] = SIRdf["Recovered_{}".format(count)]
    combined_df["Infected_{}".format(count)] = SIRdf["Infected_{}".format(count)]
    count += 1

time_list = []
for i in range(len(combined_df["av_infections"])):
    time_list.append(i)

combined_df["time"] = time_list

all_infections = combined_df[list(combined_df.filter(regex='Infected'))]
all_susceptible = combined_df[list((combined_df.filter(regex='Susceptible')))]
all_recovered = combined_df[list((combined_df.filter(regex='Recovered')))]
summary_df['time'] = combined_df["time"]
summary_df["av_infections_{}".format(size)] = all_infections.mean(axis=1)
summary_df["sd_infections_{}".format(size)] = all_infections.std(axis=1)
summary_df["av_susceptible_{}".format(size)] = all_susceptible.mean(axis=1)
summary_df["sd_susceptible_{}".format(size)] = all_susceptible.std(axis=1)
summary_df["av_recovered_{}".format(size)] = all_recovered.mean(axis=1)
summary_df["sd_recovered_{}".format(size)] = all_recovered.std(axis=1)

summary_df.to_csv(output_name, index=False)

# Create plot to show SIR curves against time
y_list = []
for i in range(10):
    y_list.append("Infected_{}".format(i))

combined_df.plot(y=y_list)
plt.savefig(os.path.join(os.path.dirname(__file__),
            infection_curve_output))

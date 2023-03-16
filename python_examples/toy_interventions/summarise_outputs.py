import os
import pandas as pd
import matplotlib.pyplot as plt

file_name = "output_4x4_av5_{}.csv"
grid_size = file_name.split('_')[1]
output_name = "simulation_outputs/summary_{}_av5.csv".format(grid_size)
infection_curve_output = \
    "simulation_outputs/{}_av5_places_plot_infections.png".format(grid_size)
size = int(grid_size.split('x')[0])
repeats = 10

combined_df = pd.DataFrame()
summary_df = pd.DataFrame()

count = 0
for i in range(repeats):
    file = file_name.format(i)
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
    SIRdf.rename(columns={"InfectionStatus.Susceptible":
                          "Susceptible_{}".format(count),
                          "InfectionStatus.Recovered":
                          "Recovered_{}".format(count),
                          "Infected": "Infected_{}".format(count)},
                 inplace=True)
    combined_df["Susceptible_{}".format(count)] = \
        SIRdf["Susceptible_{}".format(count)]
    combined_df["Recovered_{}".format(count)] = \
        SIRdf["Recovered_{}".format(count)]
    combined_df["Infected_{}".format(count)] = \
        SIRdf["Infected_{}".format(count)]
    count += 1

all_infections = combined_df[list(combined_df.filter(regex='Infected'))]
all_susceptible = combined_df[list((combined_df.filter(regex='Susceptible')))]
all_recovered = combined_df[list((combined_df.filter(regex='Recovered')))]

summary_df["av_infections_{}".format(size)] = all_infections.mean(axis=1)
summary_df["sd_infections_{}".format(size)] = all_infections.std(axis=1)
summary_df["av_susceptible_{}".format(size)] = all_susceptible.mean(axis=1)
summary_df["sd_susceptible_{}".format(size)] = all_susceptible.std(axis=1)
summary_df["av_recovered_{}".format(size)] = all_recovered.mean(axis=1)
summary_df["sd_recovered_{}".format(size)] = all_recovered.std(axis=1)

time_list = []
for i in range(len(summary_df["av_infections_{}".format(size)])):
    time_list.append(i)

combined_df["time"] = time_list
summary_df['time'] = combined_df["time"]

summary_df.to_csv(os.path.join(os.path.dirname(__file__),
                  output_name), index=False)

# Create plot to show SIR curves against time
y_list = []
for i in range(10):
    y_list.append("Infected_{}".format(i))

combined_df.plot(y=y_list)
plt.savefig(os.path.join(os.path.dirname(__file__),
            infection_curve_output))

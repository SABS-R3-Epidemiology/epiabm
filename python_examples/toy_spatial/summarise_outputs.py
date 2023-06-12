import os
import pandas as pd
import matplotlib.pyplot as plt

grid_sizes = [4, 6, 8, 12, 15]
r0 = [1, 1.5, 2, 4]

combined_summary_df = pd.DataFrame()
for r in r0:
    for element in grid_sizes:
        size = element
        file_names = ["output_{}x{}_av5_0_{}.csv".format(size, size,r), "output_{}x{}_av5_1_{}.csv".format(size, size,r), "output_{}x{}_av5_2_{}.csv".format(size, size,r), "output_{}x{}_av5_3_{}.csv".format(size, size,r), "output_{}x{}_av5_4_{}.csv".format(size, size,r)]#, "output_{}x{}_av5_5_{}.csv".format(size, size,r),
        #             "output_{}x{}_av5_6_{}.csv".format(size, size,r), "output_{}x{}_av5_7_{}.csv".format(size, size,r), "output_{}x{}_av5_8_{}.csv".format(size, size,r), "output_{}x{}_av5_9_{}.csv".format(size, size,r)]
        #file_names = ["output_{}x{}_av5_0.csv".format(size, size), "output_{}x{}_av5_1.csv".format(size, size), "output_{}x{}_av5_2.csv".format(size, size), "output_{}x{}_av5_3.csv".format(size, size), "output_{}x{}_av5_4.csv".format(size, size)]#, "output_{}x{}_av5_5_{}.csv".format(size, size,r),
        
        output_name = "simulation_outputs/new/summary_{}x{}_av5_r{}.csv".format(size, size, r)
        infection_curve_output = "simulation_outputs/new/{}x{}_av5_places_plot_infections_r{}.png".format(size, size, r)
        

        combined_df = pd.DataFrame()
        summary_df = pd.DataFrame()

        count = 0
        for file in file_names:
            filename = os.path.join(os.path.dirname(__file__), "simulation_outputs/R0",
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

        all_infections = combined_df[list(combined_df.filter(regex='Infected'))]
        all_susceptible = combined_df[list((combined_df.filter(regex='Susceptible')))]
        all_recovered = combined_df[list((combined_df.filter(regex='Recovered')))]
        
        summary_df["av_infections_{}".format(size)] = all_infections.mean(axis=1)
        summary_df["sd_infections_{}".format(size)] = all_infections.std(axis=1)
        summary_df["av_susceptible_{}".format(size)] = all_susceptible.mean(axis=1)
        summary_df["sd_susceptible_{}".format(size)] = all_susceptible.std(axis=1)
        summary_df["av_recovered_{}".format(size)] = all_recovered.mean(axis=1)
        summary_df["sd_recovered_{}".format(size)] = all_recovered.std(axis=1)

        combined_summary_df = pd.concat([combined_summary_df, summary_df], axis=1)

        time_list = []
        for i in range(len(summary_df["av_infections_{}".format(size)])):
            time_list.append(i)

        summary_df["time"] = time_list

        summary_df.to_csv(output_name, index=False)

        # Create plot to show SIR curves against time
        y_list = []
        for i in range(5):
            y_list.append("Infected_{}".format(i))

        combined_df.plot(y=y_list)
        plt.savefig(os.path.join(os.path.dirname(__file__),
                    infection_curve_output))

    combined_summary_df["time"] = time_list
    combined_summary_df.to_csv("simulation_outputs/R0/combined_summary_r{}.csv".format(r), index=False)

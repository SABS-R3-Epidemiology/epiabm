#
# Reads a csv of toy population and plots infection curves
#

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os


class Plotter():
    """Class to take a csv file and return various plots.
    """
    def __init__(self, foldername: str, grid_sizes: list, avplaces: int, repeats: int, parameter: int, parameter_values: list):
        self.folder = foldername
        self.grid_sizes = grid_sizes
        self.avplaces = avplaces
        self.repeats = repeats
        self.parameter = parameter
        self.parameter_values = parameter_values

    def _summarise_outputs(self):
        for grid_size in self.grid_sizes:
            if self.parameter is not None:
                for parameter_value in self.parameter_values:
                    file_names = ["output_{}x{}_av{}_{}{}_{}.csv".format(
                        grid_size, grid_size, self.avplaces, self.parameter,
                        parameter_value, i)
                        for i in range(self.repeats)]
                    combined_output_name = 'combined_{}x{}_av{}_{}_{}.csv'.\
                        format(grid_size, grid_size, self.avplaces,
                               self.parameter, parameter_value)
                    summary_output_name = 'summary_{}x{}_av{}_{}_{}.csv'.\
                        format(grid_size, grid_size, self.avplaces,
                               self.parameter, parameter_value)

                    self._make_and_save_outputs(
                        file_names, combined_output_name, summary_output_name)
            else:
                file_names = ["output_{}x{}_av{}_{}.csv".format(
                        grid_size, grid_size, self.avplaces, i)
                        for i in range(self.repeats)]
                combined_output_name = 'combined_{}x{}_av{}.csv'.format(
                        grid_size, grid_size, self.avplaces)
                summary_output_name = 'summary_{}x{}_av{}.csv'.format(
                        grid_size, grid_size, self.avplaces)

                self._make_and_save_outputs(
                    file_names, combined_output_name, summary_output_name)

    def _make_and_save_outputs(self, filenames, combined_name, summary_name):
        combined_df = self._combine_dataframes(filenames)
        summary_df = self._summarise_dataframes(combined_df)

        time_list = []
        for i in range(summary_df.shape[0]):
            time_list.append(i)

        combined_df["time"] = time_list
        summary_df["time"] = time_list

        # Write to output files
        combined_df.to_csv(os.path.join(os.path.dirname(__file__),
                           self.folder, combined_name), index=False)
        summary_df.to_csv(os.path.join(os.path.dirname(__file__),
                          self.folder, summary_name), index=False)

    def _combine_dataframes(self, filenames: list):
        combined_df = pd.DataFrame()
        for i in range(len(filenames)):
            file = filenames[i]
            filename = os.path.join(os.path.dirname(__file__), self.folder,
                                    file)

            SIRdf = pd.read_csv(filename)
            total = SIRdf[list(SIRdf.filter(regex='InfectionStatus.Infect'))]
            SIRdf["Infected"] = total.sum(axis=1)
            SIRdf = SIRdf.groupby(
                ["time"]).agg({"InfectionStatus.Susceptible": 'sum',
                               "Infected": 'sum',
                               "InfectionStatus.Recovered": 'sum',
                               "InfectionStatus.Dead": 'sum'})
            SIRdf.rename(columns={"InfectionStatus.Susceptible":
                                  "Susceptible_{}".format(i),
                                  "InfectionStatus.Recovered":
                                  "Recovered_{}".format(i),
                                  "Infected":
                                  "Infected_{}".format(i)},
                         inplace=True)
            combined_df["Susceptible_{}".format(i)] = \
                SIRdf["Susceptible_{}".format(i)]
            combined_df["Recovered_{}".format(i)] = \
                SIRdf["Recovered_{}".format(i)]
            combined_df["Infected_{}".format(i)] = \
                SIRdf["Infected_{}".format(i)]

        return combined_df

    def _summarise_dataframes(self, combined_df):
        summary_df = pd.DataFrame()
        all_infections = combined_df[
            list(combined_df.filter(regex='Infected'))]
        all_susceptible = combined_df[
            list((combined_df.filter(regex='Susceptible')))]
        all_recovered = combined_df[
            list((combined_df.filter(regex='Recovered')))]

        summary_df["av_infections"] = all_infections.mean(axis=1)
        summary_df["sd_infections"] = all_infections.std(axis=1)
        summary_df["av_susceptible"] = all_susceptible.mean(axis=1)
        summary_df["sd_susceptible"] = all_susceptible.std(axis=1)
        summary_df["av_recovered"] = all_recovered.mean(axis=1)
        summary_df["sd_recovered"] = all_recovered.std(axis=1)

        return summary_df

    def _plot_SIR(self, combined_df_name):
        name = combined_df_name.replace('combined', '')
        name = name.replace('.csv', '')
        plot_name = 'plot_infections_{}.png'.format(name)

        combined_df = pd.read_csv(os.path.join(os.path.dirname(__file__),
                                  self.folder, combined_df_name))

        # Create plot to show SIR curves against time
        y_list = []
        for i in range(10):
            y_list.append("Infected_{}".format(i))

        combined_df.plot(y=y_list)
        plt.savefig(os.path.join(os.path.dirname(__file__), self.folder,
                    plot_name))

    def _multiple_curve_plotter(self, name_fig=None):
        color_list = list(mcolors.BASE_COLORS.keys())
        count = 0
        for grid_size in self.grid_sizes:
            if self.parameter is not None:
                for parameter_value in self.parameter_values:
                    summary_output_name = 'summary_{}x{}_av{}_{}_{}.csv'.\
                        format(grid_size, grid_size, self.avplaces,
                               self.parameter, parameter_value)
                    label = '{}x{}, {}:{}'.format(
                        grid_size, grid_size, self.parameter, parameter_value)
                
                    plot = self._make_multiple_curve_plot(
                        summary_output_name, color_list[count], label)
                    count += 1
            else:
                summary_output_name = 'summary_{}x{}_av{}.csv'.format(
                        grid_size, grid_size, self.avplaces)
                label = '{}x{}'.format(grid_size, grid_size)

                plot = self._make_multiple_curve_plot(
                    summary_output_name, color_list[count], label)
                count += 1

        if name_fig is None:
            name_fig = 'plot_summary'

        plot.legend()
        plot.savefig(os.path.join(os.path.dirname(__file__), self.folder,
                     '{}.png'.format(name_fig)))

    def _make_multiple_curve_plot(self, summary_output_name, color, label):
        summary_df = pd.read_csv(os.path.join(os.path.dirname(__file__),
                                 self.folder, summary_output_name))

        plt.plot(summary_df['time'], summary_df['av_infections'],
                 '{}-'.format(color), label=label)
        plt.fill_between(
            summary_df['time'],
            summary_df['av_infections'] - summary_df['sd_infections'],
            summary_df['av_infections'] + summary_df['sd_infections'],
            color=color, alpha=0.2)
        return plt

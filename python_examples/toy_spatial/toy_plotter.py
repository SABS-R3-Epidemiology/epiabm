#
# Plot the infection curves
#

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


class Plotter():
    """Class to visualise simulation outputs.
    """
    def __init__(self, foldername: str, grid_size: int, repeats: int,
                 sim_parameters: dict, sim_parameters_labels: list):
        """Initialise the plotter with simulation information

        Parameters
        ----------
        foldername : str
            Name of the output folder of simulations
        grid_size : int
            Size of the grid used for the population set up
        repeats : int
            Number of simulation repeats 
        sim_parameters : dict
            Containing modified parameters during simulation
        sim_parameters_labels : list
            Names for the simulations.
        """
        self.folder = foldername
        self.grid_size = grid_size
        self.repeats = repeats
        self.sim_parameters = sim_parameters
        self.sim_parameters_labels = sim_parameters_labels

    def _summarise_outputs(self):
        """Summarise output of the repeats of one type of simulation.

        Returns
        ----------
        dict
            Containing the summary DataFrames per type of simulation.
        """
        dict_summary = {}
        for j in range(len(self.sim_parameters)):
            file_names = [f"output_{self.grid_size}x{self.grid_size}" +
                          f"_{self.sim_parameters_labels[j]}_rep{i}_.csv"
                          for i in range(self.repeats)]
            combined_df = self._combine_dataframes(file_names)
            summary_df = self._summarise_dataframes(combined_df)

            time_list = []
            for i in range(summary_df.shape[0]):
                time_list.append(i)
            summary_df["time"] = time_list

            dict_summary[self.sim_parameters_labels[j]] = summary_df

        return dict_summary

    def _combine_dataframes(self, filenames):
        """Store simulation output of the repeats.

        Parameters
        ----------
        filenames : list
            Names of the files containing the simulation output.

        Returns
        ----------
        pd.DataFrame
            Containing simulation output for all repeats.
        """
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
        """Determine mean and standard deviation of the repeats.

        Parameters
        ----------
        combined_df : pd.DataFrame
            Containing simulation output for all repeats.

        Returns
        ----------
        pd.DataFrame
            Containing mean and standard deviation of simulation output over repeats.
        """

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

    def _multiple_curve_plotter(self, dict_df, name_fig=None):
        """Plots the infections curves with standard deviations of
        the simulations.

        Parameters
        ----------
        dict_df : dict
            Containing the summary DataFrames per type of simulation.
        name_fig : str or None
            If provided the figure will be saved, if not figure is returned

        """
        color_dict = {4: ['blue', 'darkblue', 'deepskyblue', 'slategrey',
                          'turquoise', 'teal']}
        color_list = color_dict[self.grid_size]
        for j in range(len(self.sim_parameters)):
            df = dict_df[self.sim_parameters_labels[j]]
            label = f'{self.sim_parameters_labels[j]}'
            plt.plot(df['time'], df['av_infections'], color=color_list[j],
                     linestyle='-', label=label)
            plt.fill_between(df['time'],
                             df['av_infections'] - df['sd_infections'],
                             df['av_infections'] + df['sd_infections'],
                             color=color_list[j], alpha=0.2)

        plt.legend(loc='upper right', fontsize=8)
        plt.xlabel('Time (days)')
        plt.ylabel('Number of infected individuals')

        if name_fig:
            plt.savefig(os.path.join(os.path.dirname(__file__), self.folder,
                        '{}.png'.format(name_fig)))
        else:
            plt.show()

    def _total_recovered_bars(self, dict_df, pop_size=10000, name_fig=None):
        """Plots the total number of infections over the total simulation

        Parameters
        ----------
        dict_df : dict
            Containing the summary DataFrames per type of simulation.
        pop_size : int
            Population size of the simulation
        name_fig : str or None
            If provided the figure will be saved, if not figure is returned

        """
        color_dict = {4: ['blue', 'darkblue', 'deepskyblue', 'slategrey',
                          'turquoise', 'teal']}
        dict_info = {}
        for j in range(len(self.sim_parameters)):
            df = dict_df[self.sim_parameters_labels[j]]
            dict_info[self.sim_parameters_labels[j]] = {'mean': [],
                                                        'stdev': []}

        for j in range(len(self.sim_parameters)):
            mean = df['av_recovered'].iloc[-1]
            stdev = df['sd_recovered'].iloc[-1]
            dict_info[self.sim_parameters_labels[j]][
                'mean'].append(100/pop_size*mean)
            dict_info[self.sim_parameters_labels[j]][
                'stdev'].append(100/pop_size*stdev)
        if name_fig is None:
            name_fig = 'plot_summary'

        width = 1/(len(self.sim_parameters_labels)+1)  # the width of the bars
        multiplier = 0

        fig, ax = plt.subplots()

        highest_value = 0
        for sim_name, dict_ms in dict_info.items():
            offset = width * multiplier
            rects = ax.bar(offset, dict_ms['mean'], width,
                           yerr=dict_ms['stdev'], label=[sim_name],
                           color=[color_dict[4][multiplier]])
            ax.bar_label(rects, padding=3, fontsize=8)
            multiplier += 1
            if max(dict_ms['mean']) > highest_value:
                highest_value = max(dict_ms['mean'])

        ax.set_ylabel('Total percentage population infected')
        ax.set_xticks([0.25],
                      [f'{self.grid_size}x{self.grid_size}'])
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.85, box.height])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=8)
        if name_fig:
            plt.savefig(os.path.join(os.path.dirname(__file__), self.folder,
                                     '{}.png'.format(name_fig)))
        else:
            plt.show()

    def _summary_table(self, dict_df, tab_name=None):
        """Summarises the total number of infections over the total simulation

        Parameters
        ----------
        dict_df : dict
            Containing the summary DataFrames per type of simulation.
        tab_name : str or None
            If provided the pd.DataFrame is stored

        Returns
        -------
        pd.DataFrame
            Containing the total number of infections and peak of infection
            information of the different simulations.

        """
        pop_size = 10000
        dict_sum = {'simulation': [],
                    'percentage_mean_infections': [],
                    'percentage_sd_infections': [],
                    'height_peak': [],
                    'time_peak': []}
        for j in range(len(self.sim_parameters)):
            df = dict_df[self.sim_parameters_labels[j]]
            mean = df['av_recovered'].iloc[-1]
            stdev = df['sd_recovered'].iloc[-1]

            max_height = df['av_infections'].max()
            max_time = df[df['av_infections'] == max_height].iloc[0]['time']

            dict_sum['simulation'].append(self.sim_parameters_labels[j])
            dict_sum['percentage_mean_infections'].append(100/pop_size*mean)
            dict_sum['percentage_sd_infections'].append(100/pop_size*stdev)
            dict_sum['height_peak'].append(max_height)
            dict_sum['time_peak'].append(max_time)
        df_sum = pd.DataFrame.from_dict(dict_sum)

        if tab_name:
            df_sum.to_csv(os.path.join(os.path.dirname(__file__), self.folder,
                          '{}.csv'.format(tab_name)), index=False)

        return df_sum

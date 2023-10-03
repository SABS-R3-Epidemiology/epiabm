#
# Plot the infection curves
#

import pandas as pd
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
                                  "Infected_{}".format(i),
                                  "InfectionStatus.Dead":
                                  "Dead_{}".format(i)},
                         inplace=True)
            combined_df["Susceptible_{}".format(i)] = \
                SIRdf["Susceptible_{}".format(i)]
            combined_df["Recovered_{}".format(i)] = \
                SIRdf["Recovered_{}".format(i)]
            combined_df["Infected_{}".format(i)] = \
                SIRdf["Infected_{}".format(i)]
            combined_df["Dead_{}".format(i)] = \
                SIRdf["Dead_{}".format(i)]

            # Total infected is sum of infections, recovered and dead
            combined_df["Total_infected_{}".format(i)] = \
                combined_df["Recovered_{}".format(i)] + \
                combined_df["Infected_{}".format(i)] + \
                combined_df["Dead_{}".format(i)]

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
            Containing mean and standard deviation of simulation output over
            repeats.
        """

        summary_df = pd.DataFrame()
        all_infections = combined_df[
            list(combined_df.filter(regex='Infected'))]
        all_susceptible = combined_df[
            list((combined_df.filter(regex='Susceptible')))]
        all_recovered = combined_df[
            list((combined_df.filter(regex='Recovered')))]
        all_dead = combined_df[
            list((combined_df.filter(regex='Dead')))]
        all_total_infected = combined_df[
            list((combined_df.filter(regex='Total_infected')))]

        summary_df["av_infections"] = all_infections.mean(axis=1)
        summary_df["sd_infections"] = all_infections.std(axis=1)
        summary_df["av_susceptible"] = all_susceptible.mean(axis=1)
        summary_df["sd_susceptible"] = all_susceptible.std(axis=1)
        summary_df["av_recovered"] = all_recovered.mean(axis=1)
        summary_df["sd_recovered"] = all_recovered.std(axis=1)
        summary_df["av_dead"] = all_dead.mean(axis=1)
        summary_df["sd_dead"] = all_dead.std(axis=1)
        summary_df["av_total_infected"] = all_total_infected.mean(axis=1)
        summary_df["sd_total_infected"] = all_total_infected.std(axis=1)

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

        plt.figure(figsize=(5, 4.8))

        # Get data and make figure
        for j in range(len(self.sim_parameters)):
            df = dict_df[self.sim_parameters_labels[j]]
            label = f'{self.sim_parameters_labels[j]}'
            plt.plot(df['time'], df['av_infections'], color=color_list[j],
                     linestyle='-', label=label)
            plt.fill_between(df['time'],
                             df['av_infections'] - df['sd_infections'],
                             df['av_infections'] + df['sd_infections'],
                             color=color_list[j], alpha=0.2)

        plt.legend(loc='upper right', fontsize=12)
        plt.xlabel('Time (days)', fontsize=12)
        plt.ylabel('Number of infected individuals', fontsize=12)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)

        if name_fig:
            plt.title('a', loc='left', weight='bold', fontsize=12)
            plt.tight_layout()
            plt.savefig(os.path.join(os.path.dirname(__file__), self.folder,
                        '{}.png'.format(name_fig)), dpi=300)
        else:
            plt.show()

    def _total_infected_bars(self, dict_df, pop_size=10000, name_fig=None):
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

        # Get the mean and standard deviation over repeats
        mean_list = []
        std_list = []
        for j in range(len(self.sim_parameters)):
            df = dict_df[self.sim_parameters_labels[j]]
            mean_list.append(100/pop_size*df['av_total_infected'].iloc[-1])
            std_list.append(100/pop_size*df['sd_total_infected'].iloc[-1])

        fig, ax = plt.subplots(figsize=(5, 4.8))

        # Make figure
        rects = ax.bar(self.sim_parameters_labels, mean_list, yerr=std_list,
                       color=color_dict[4])
        ax.bar_label(rects, padding=3, fontsize=12)

        ax.set_ylabel('Total population infected (percentage)', fontsize=12)
        ax.tick_params(axis='x', labelsize=11)
        ax.tick_params(axis='y', labelsize=12)
        ax.set_ylim(top=110)

        if name_fig:
            ax.set_xlabel(' ', fontsize=12)
            plt.title('b', loc='left', weight='bold', fontsize=12)
            plt.tight_layout()
            plt.savefig(os.path.join(os.path.dirname(__file__), self.folder,
                                     '{}.png'.format(name_fig)), dpi=300)
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
            mean = df['av_total_infected'].iloc[-1]
            stdev = df['sd_total_infected'].iloc[-1]

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

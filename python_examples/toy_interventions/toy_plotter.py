#
# Reads a csv of toy population and plots infection curves
#

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib as mpl
import os

class Plotter():
    """Class to take a csv file and return various plots.
    """
    def __init__(self, foldername: str, grid_sizes: list, avplaces: int,
                 repeats: int, parameter_sets_list: list,
                 parameter_sets_labels: list):
        self.folder = foldername
        self.grid_sizes = grid_sizes
        self.avplaces = avplaces
        self.repeats = repeats
        # self.intervention = intervention
        # self.parameter = parameter
        # self.parameter_values = parameter_values
        self.parameter_sets_list = parameter_sets_list
        self.parameter_sets_labels = parameter_sets_labels


    def _summarise_outputs(self):
        for grid_size in self.grid_sizes:
            # if self.parameter:
            #     for parameter_value in self.parameter_values:
            #         file_names = ["output_{}x{}_av{}_{}_{}_{}_{}.csv".format(
            #             grid_size, grid_size, self.avplaces, self.intervention,
            #             self.parameter, parameter_value, i)
            #             for i in range(self.repeats)]
            #         combined_output_name = 'combined_{}x{}_av{}_{}_{}_{}.csv'.\
            #             format(grid_size, grid_size, self.avplaces,
            #                    self.intervention, self.parameter,
            #                    parameter_value)
            #         summary_output_name = 'summary_{}x{}_av{}_{}_{}_{}.csv'.\
            #             format(grid_size, grid_size, self.avplaces,
            #                    self.intervention, self.parameter,
            #                    parameter_value)

            #         self._make_and_save_outputs(
            #             file_names, combined_output_name, summary_output_name)
            if len(self.parameter_sets_list) > 0:
                for j in range(len(self.parameter_sets_list)):
                    file_names = ["output_{}x{}_av{}_{}_{}.csv".format(
                            grid_size, grid_size, self.avplaces,
                            self.parameter_sets_labels[j], i)
                            for i in range(self.repeats)]
                    combined_output_name = 'combined_{}x{}_av{}_{}.csv'.format(
                        grid_size, grid_size, self.avplaces,
                        self.parameter_sets_labels[j])
                    summary_output_name = 'summary_{}x{}_av{}_{}.csv'.format(
                        grid_size, grid_size, self.avplaces,
                        self.parameter_sets_labels[j])
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
        for i in range(self.repeats):
            y_list.append("Infected_{}".format(i))

        combined_df.plot(y=y_list)
        plt.savefig(os.path.join(os.path.dirname(__file__), self.folder,
                    plot_name))

    def _multiple_curve_plotter(self, name_fig=None):
        color_dict = {4: ['blue', 'darkblue', 'deepskyblue', 'slategrey', 'turquoise', 'teal'],
                      15: ['red', 'darkred', 'mediumvioletred', 'violet', 'hotpink', 'darkmagenta']}
        for grid_size in self.grid_sizes:
            color_list = color_dict[grid_size]
            count = 0
            # if self.parameter:
            #     for parameter_value in self.parameter_values:
            #         summary_output_name = 'summary_{}x{}_av{}_{}_{}_{}.csv'.\
            #             format(grid_size, grid_size, self.avplaces,
            #                    self.intervention, self.parameter,
            #                    parameter_value)
            #         label = '{}x{}, {}:{}'.format(
            #             grid_size, grid_size, self.parameter, parameter_value)

            #         plot = self._make_multiple_curve_plot(
            #             summary_output_name, color_list[count], label)
            #         count += 1
            #     title = ' {}'.format(self.intervention)
            if len(self.parameter_sets_list) > 0:
                for j in range(len(self.parameter_sets_list)):
                    summary_output_name = 'summary_{}x{}_av{}_{}.csv'.\
                        format(grid_size, grid_size, self.avplaces,
                               self.parameter_sets_labels[j])
                    # label = '{}x{}, {}'.format(
                    #     grid_size, grid_size, self.parameter_sets_labels[j])
                    label = f'{self.parameter_sets_labels[j]}'
                    plot = self._make_multiple_curve_plot(
                        summary_output_name, color_list[count], label)
                    count += 1
                # title = ' {}'.format(self.intervention)
                title = ''
            else:
                summary_output_name = 'summary_{}x{}_av{}.csv'.format(
                        grid_size, grid_size, self.avplaces)
                label = '{}x{}'.format(grid_size, grid_size)

                plot = self._make_multiple_curve_plot(
                    summary_output_name, color_list[count], label)
                count += 1
                title = ''

        if name_fig is None:
            name_fig = 'plot_summary'

        plot.legend(loc='upper right', fontsize=8)
        # plot.legend(fontsize=8)
        plot.xlabel('Time (days)')
        plot.ylabel('Number of infected individuals')
        # plot.title('Infection curve{}'.format(title))
        plot.savefig(os.path.join(os.path.dirname(__file__), self.folder,
                     '{}.png'.format(name_fig)))

    def _make_multiple_curve_plot(self, summary_output_name, color, label):
        summary_df = pd.read_csv(os.path.join(os.path.dirname(__file__),
                                 self.folder, summary_output_name))

        plt.plot(summary_df['time'], summary_df['av_infections'],
                 color=color, linestyle='-', label=label)
        plt.fill_between(
            summary_df['time'],
            summary_df['av_infections'] - summary_df['sd_infections'],
            summary_df['av_infections'] + summary_df['sd_infections'],
            color=color, alpha=0.2)
        return plt

    def _total_recovered_bars(self, name_fig, pop_size =10000):
        color_dict = {4: ['blue', 'darkblue', 'deepskyblue', 'slategrey', 'turquoise', 'teal'],
                      15: ['red', 'darkred', 'mediumvioletred', 'violet', 'hotpink', 'darkmagenta']}
        
        grids = [f'{str(x)}x{str(x)}' for x in self.grid_sizes]
        dict_info = {}
        for j in range(len(self.parameter_sets_list)):
            dict_info[self.parameter_sets_labels[j]] = {'mean': [], 'stdev': []}

        for grid_size in self.grid_sizes:
            if len(self.parameter_sets_list) > 0:
                for j in range(len(self.parameter_sets_list)):
                    summary_output_name = 'summary_{}x{}_av{}_{}.csv'.\
                        format(grid_size, grid_size, self.avplaces,
                               self.parameter_sets_labels[j])
                    mean, stdev = self._store_recovered_bar_plot(summary_output_name)
                    dict_info[self.parameter_sets_labels[j]]['mean'].append(100/pop_size*mean)
                    dict_info[self.parameter_sets_labels[j]]['stdev'].append(100/pop_size*stdev)
        if name_fig is None:
            name_fig = 'plot_summary'

        x = np.arange(len(grids))  # the label locations
        width = 1/(len(self.parameter_sets_labels)+1)  # the width of the bars
        multiplier = 0

        fig, ax = plt.subplots()

        highest_value = 0
        for sim_name, dict_ms in dict_info.items():
            offset = width * multiplier
            rects = ax.bar(x + offset, dict_ms['mean'], width, yerr=dict_ms['stdev'], label=[sim_name], color=[color_dict[4][multiplier]])
            ax.bar_label(rects, padding=3, fontsize=8)
            multiplier += 1
            if max(dict_ms['mean']) > highest_value:
                highest_value = max(dict_ms['mean'])

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Total percentage population infected')
        # ax.set_title('Total infections')
        ax.set_xticks(x + ((len(x)-1)*0.5*width) , grids)
        # Set only y range when highest value above 50%
        if highest_value > 50: 
            ax.set_ylim(0, 110)
        # ax.legend()
        # ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
        #   fancybox=True, shadow=True, ncol=len(self.parameter_sets_labels)*2)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.85, box.height])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=8)
        plt.savefig(os.path.join(os.path.dirname(__file__), self.folder,
                    '{}.png'.format(name_fig)))

    def _store_recovered_bar_plot(self, input_file):
        summary_df = pd.read_csv(os.path.join(os.path.dirname(__file__),
                                 self.folder, input_file))
        return summary_df['av_recovered'].iloc[-1], summary_df['sd_recovered'].iloc[-1]

    def _summary_table(self, name):
        pop_size = 10000
        dict_sum = {'grid': [],
                    'run': [],
                    'percentage_mean_infections': [],
                    'percentage_sd_infections': [],
                    'height_peak': [],
                    'time_peak': []}
        for grid_size in self.grid_sizes:
            for j in range(len(self.parameter_sets_list)):
                summary_output_name = 'summary_{}x{}_av{}_{}.csv'.\
                        format(grid_size, grid_size, self.avplaces,
                               self.parameter_sets_labels[j])
                df = pd.read_csv(os.path.join(os.path.dirname(__file__), self.folder, summary_output_name))
                mean, stdev = self._store_recovered_bar_plot(summary_output_name)
                df['av_infections'] = df['av_infections'].astype(float)
                df['time'] = df['time'].astype(int)

                max_height = df['av_infections'].max()
                max_time = df[df['av_infections']==max_height].iloc[0]['time']

                dict_sum['grid'].append(grid_size)
                dict_sum['run'].append(self.parameter_sets_labels[j])
                dict_sum['percentage_mean_infections'].append(100/pop_size*mean)
                dict_sum['percentage_sd_infections'].append(100/pop_size*stdev)
                dict_sum['height_peak'].append(max_height)
                dict_sum['time_peak'].append(max_time)
        df_sum = pd.DataFrame.from_dict(dict_sum)
        df_sum.to_csv(os.path.join(os.path.dirname(__file__), self.folder,
                      '{}.csv'.format(name)), index=False)


                

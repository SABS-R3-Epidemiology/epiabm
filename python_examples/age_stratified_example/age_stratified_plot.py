#
# Reads a csv of age stratified data and plots as a bar chart

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# csv input files should have the column headers:
# time, infection_Status1, infection_status2, ..., age_range
# so there will be multiple entries for each timepoint.


class Plotter():
    """Class to take a csv file and return various plots,
    including the capability to make an age-statified
    bar chart.
    """
    def __init__(self, filepath: str, start_date=None, sum_weekly=False,
                 age_list: list = None):
        """Initialise the plotter with a filepath and read
        data from the csv.
        Parameters
        ----------
        filepath : str
            Filepath to the .csv containing output data
        start_date : str
            Starting date for the simulation, "day-month-year"
        sum_weekly : bool
            Flag to plot either each timepoint, or the 7 day sum
        age_list : list
            List of the explicit age ranges saved in the csv
        """
        if not os.path.splitext(filepath)[1] == ".csv":
            raise TypeError("input file" + filepath + "must be .csv")
        self.data = pd.read_csv(filepath)
        self.age_list = age_list
        self.start_date = start_date
        self.sum_weekly = sum_weekly

        # Identify the column containing age stratification as any
        # with the substring "age"
        self.age_name = next((s for s in list(self.data.columns)
                             if "age" in s.lower()), None)
        self.do_ages = (self.age_name is not None)
        if self.do_ages and (self.age_list is None):
            num = self.data[self.age_name].max()
            self.age_list = [str(5*i)+"-"+str(5*i+5) for i in range(num+1)]

    def _sum_infectious(self) -> None:
        """Helper function which sums across all columns containing infectious
        people and appends the dataframe with a further column containing this
        data.
        """
        total = self.data[list(self.data.
                               filter(regex='InfectionStatus.Infect'))]
        self.data["Total Infectious"] = total.sum(axis=1)

    def _dates(self, dataFrame=None, period='weekly') -> None:
        """Helper function to calculate a dictionary associating each
        timestep, with the date of a day, or week.
        Parameters
        ----------
        dataFrame : DataFrame
            dataFrame containing a "time" column
        period : str
            Either "daily" or "weekly"

        Returns
        -------
        date_list: list
            List of dates, corresponding to the time column
        """
        assert self.start_date is not None, 'Start date not set'
        assert period in ['daily', 'weekly'], 'Period not daily or weekly'
        if dataFrame is None:
            dataFrame = self.data
        date_list = []
        timepoints = list(dataFrame['time'])
        start = pd.to_datetime(self.start_date).date()
        for time in timepoints:
            if period == 'daily':
                date_list.append((start + pd.DateOffset(days=time)).date())
            else:
                if time % 7 == 0:
                    week_date = (start + pd.DateOffset(days=time)).date()
                date_list.append(week_date)
        date_list = [d.strftime('%m-%d') for d in date_list]
        return date_list

    def _5yrAgeGroupsTo10(self):
        """Helper function which assumes data is given in equally spaced
        age groups of 5 year gaps. Returns data redistributed into 10 year
        age gaps. Dataframe must have age groups on separate rows indexed
        by numbers.
        """
        dataframe = self.data.copy()
        num_10yr = np.ceil(len(self.age_list)/2)
        indexCol = [np.floor(i/2) for i in dataframe[self.age_name]]
        dataframe[self.age_name] = indexCol
        self.age_list = [str(10*i)+"-"+str(10*i+10) for i
                         in range(int(num_10yr+1))]
        self.data = dataframe

    def barchart(self, outfile: str,
                 infection_category: str = "Total Infectious",
                 write_Df_toFile=None):
        """Function which creates a bar chart from csv data, with
        capability to stratify by age if required. Plot is automatically
        saved to a png file.
        Parameters
        ----------
        outfile : str
            Path to the .png file where the bar chart will be saved
        infection_category : str
            Category to be plotted, defaults to Total Infectious
        write_Df_toFile : str
            Optional argument, .csv filepath if configured plotting
            data should be written to file
        """
        if infection_category == "Total Infectious":
            self._sum_infectious()
        if self.do_ages and self.age_list[0] == '0-5':
            # If data is presented in 5 year age groups.
            self._5yrAgeGroupsTo10()
        new_frame = self.data.loc[:, ('time', infection_category)]
        time_col = 'time'
        if self.start_date is not None:
            # If a start date is given, plot with dates on x axis.
            time_col = 'dates'
            if self.sum_weekly:
                # By giving the same 'dates' for each weekday, the
                # 7 day total is automatically found.
                new_frame['dates'] = self._dates(new_frame, 'weekly')
            else:
                new_frame['dates'] = self._dates(new_frame, 'daily')

        if self.do_ages:
            # If we have age stratified data, plot the bar chart with
            # colours for each age.
            new_frame.loc[:, self.age_name] = self.data.loc[:, self.age_name]
            new_frame = new_frame.groupby([time_col, self.age_name]) \
                .sum().reset_index()
            new_frame = new_frame.pivot(index=time_col, columns=self.age_name,
                                        values=infection_category)
            if self.age_list:
                # Renames columns to actual age ranges if given.
                idx = list(new_frame.columns)[0]
                for i in range(len(list(new_frame.columns))):
                    new_frame = new_frame \
                                    .rename(columns={i+idx: self.age_list[i]})
            if write_Df_toFile is not None:
                new_frame.to_csv(write_Df_toFile)
            new_frame.plot.bar(stacked=True, colormap="inferno_r")
        else:
            new_frame = new_frame.groupby([time_col]) \
                .sum().reset_index()
            new_frame.plot.bar(x=time_col, y=infection_category)
        if self.sum_weekly:
            title = "Weekly Cases by age"
        else:
            title = "Daily Cases by age"
        plt.title(title)
        plt.gca().legend().set_title('')
        plt.xlabel("Time")
        plt.savefig(outfile)


if __name__ == '__main__':
    dirname = os.path.dirname(os.path.abspath(__file__))
    p = Plotter(os.path.join(os.path.dirname(__file__),
                "comparison_outputs/output_gibraltar.csv"),
                start_date='01-01-2020', sum_weekly=False)
    p.barchart(os.path.join(os.path.dirname(__file__),
               "comparison_outputs/age_stratify.png"),
               write_Df_toFile=os.path.join(os.path.dirname(__file__),
               "comparison_outputs/gibraltar_daily_cases.csv"))

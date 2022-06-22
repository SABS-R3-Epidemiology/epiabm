#
# Reads a csv of age stratified data and plots as a bar chart

import pandas as pd
import matplotlib.pyplot as plt
import os

# csv input files should have the column headers:
# time, infection_Status1, infection_status2, ..., age_range
# so there will be multiple entries for each timepoint.


class Plotter():
    """Funtion to take a csv file and return various plots,
    including the capability to make an age-statified
    bar chart.
    """
    def __init__(self, filepath: str, age_list: list = None):
        """Initialise the plotter with a filepath and read
        data from the csv

        Parameters
        ----------
        filepath : str
            Filepath to the .csv containing output data
        age_list : list
            List of the explicit age ranges saved in the csv
        """
        if not os.path.splitext(filepath)[1] == ".csv":
            raise TypeError("input file" + filepath + "must be .csv")
        self.data = pd.read_csv(filepath)
        self.age_list = age_list

        # Identify the column containing age stratifcation as any
        # with the substring "age"
        self.age_name = next((s for s in list(self.data.columns)
                             if "age" in s.lower()), None)
        self.do_ages = (self.age_name is not None)
        if self.do_ages and (self.age_list is None):
            num = self.data[self.age_name].max()
            self.age_list = ["{}0-{}0".format(i, i+1) for i in range(num+1)]

    def sum_infectious(self) -> None:
        """Helper function which sums across all columns containing infectious
        people and appends the dataframe with a further column containing this
        data. Assumes infection status columns are next to each other.
        """
        i1 = list(self.data.columns).index("InfectionStatus.InfectASympt")
        i2 = list(self.data.columns).index("InfectionStatus.InfectICURecov")
        self.data["Total Infectious"] = self.data.iloc[:, i1:i2+1].sum(axis=1)

    def barchart(self, outfile: str,
                 infection_category: str = "Total Infectious"):
        """Function which creates a bar chart from csv data, with
        capability to stratify by age if required. Plot is automatically
        saved to a png file.

        Parameters
        ----------
        outfile : str
            Path to the .png file where the bar chart will be saved
        infection_category : str
            Category to be plotted, defaults to Total Infectious

        """
        if infection_category == "Total Infectious":
            self.sum_infectious()
        new_frame = self.data.loc[:, ('time', infection_category)]
        if self.do_ages:
            new_frame.loc[:, self.age_name] = self.data.loc[:, self.age_name]
            new_frame = new_frame.groupby(["time", self.age_name]) \
                .sum().reset_index()
            print(new_frame)
            new_frame = new_frame.pivot(index="time", columns=self.age_name,
                                        values=infection_category)
            if self.age_list:
                # Renames columns to actual age ranges if given.
                for i in range(len(list(new_frame.columns))):
                    new_frame = new_frame.rename(columns={i: self.age_list[i]})
            new_frame.plot.bar(stacked=True, colormap="inferno_r")
        else:
            new_frame.plot.bar(x='time', y=infection_category)
        plt.title("Infections, stratified by age")
        plt.xlabel("Time")
        plt.ylabel("Number infected")
        plt.savefig(outfile)


if __name__ == '__main__':
    dirname = os.path.dirname(os.path.abspath(__file__))
    p = Plotter(os.path.join(dirname, "output.csv"))
    p.barchart(os.path.join(dirname, "age_stratify.png"))
    plt.show()

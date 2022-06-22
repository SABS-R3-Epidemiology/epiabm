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
    def __init__(self, filepath: str):
        if not os.path.splitext(filepath)[1] == ".csv":
            raise TypeError("input file" + filepath + "must be .csv")
        self.filepath = filepath
        self.data = pd.read_csv(filepath)
        self.do_ages = ("AgeRange" in list(self.data.columns))
        print(self.do_ages)
        
    def sum_infectious(self) -> None:
        '''Helper function which sums across all columns containing infectious
        people and appends the dataframe with a further column containing this
        data.
        '''
        ind1 = list(self.data.columns).index("InfectionStatus.InfectASympt")
        ind2 = list(self.data.columns).index("InfectionStatus.InfectICURecov")
        self.data["Total Infectious"] = self.data.iloc[:, ind1:ind2+1].sum(axis=1)

    def barchart(self, outfile: str,
                 infection_category: str = "Total Infectious"):
        """Function which creates a bar chart from csv data, with
        capability to stratify by age if required.

        Parameters
        ----------
        infection_category : str
            Category to be plotted, includes 

        """
        if infection_category == "Total Infectious":
            self.sum_infectious()
        new_frame = self.data.loc[:, ('time', infection_category)]
        if self.do_ages:
            new_frame.loc[:, "AgeRange"] = self.data.loc[:, "AgeRange"]
            new_frame = new_frame.pivot(index="time", columns='AgeRange',
                                        values=infection_category)
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

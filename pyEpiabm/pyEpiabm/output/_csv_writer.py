#
# Write data in a list to a csv file
#

import csv
import typing
import os

from pyEpiabm.output.abstract_reporter import AbstractReporter


class _CsvWriter(AbstractReporter):
    def __init__(self, folder: str, filename: str, fieldnames: typing.List,
                 clear_folder: bool = False):
        """Initialises a file to store output in, and which categories
        to record.

        Parameters
        ----------
        folder : str
            Output folder path
        filename : str
            Output file name
        fieldnames : typing.List
            List of categories to be saved
        clear_folder : bool
            Whether to empty the folder before saving results

        """
        super().__init__(folder, clear_folder)

        self.f = open(os.path.join(folder, filename), 'w')
        self.writer = csv.writer(
            self.f, delimiter=',')
        self.writer.writerow(fieldnames)

    def __del__(self):
        """Closes the file when the simulation is finished.
        Required for file data to be further used.

        """
        if self.f:
            self.f.close()

    def write(self, row: typing.List):
        """Writes data to file.

        Parameters
        ----------
        row : typing.List
            List of data to be saved

        """
        self.writer.writerow(row)

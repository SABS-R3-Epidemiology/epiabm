#
# Write data in a dict to a csv file
#

import csv
import zipfile
import typing
import os

from pyEpiabm.output.abstract_reporter import AbstractReporter


class _ZipCsvDictWriter(AbstractReporter):
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

        self.zip_buffer = zipfile.ZipFile(os.path.join(folder, filename + '.zip'), 'w')
        self.f = self.zip_buffer.open(filename, 'w')
        self.writer = csv.DictWriter(
            self.f, fieldnames=fieldnames, delimiter=',')
        self.writer.writeheader()

    def __del__(self):
        """Closes the file when the simulation is finished.
        Required for file data to be further used.

        """
        if self.f:
            self.f.close()

        self.zip_buffer.close()

    def write(self, row: typing.Dict):
        """Writes data to file.

        Parameters
        ----------
        row : dict
            Dictionary of data to be saved

        """
        self.writer.writerow(row)

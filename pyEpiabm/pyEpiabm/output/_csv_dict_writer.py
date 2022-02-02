#
# Write data in a dict to a csv file
#

import csv
import typing

from pyEpiabm.output.abstract_reporter import AbstractReporter


class _CsvDictWriter(AbstractReporter):
    def __init__(self, folder: str, filename: str, fieldnames: typing.List,
                 clear_folder: bool = True):
        """Initialises a file to store output in, and which categories
        to record.

        :param folder: Output folder path
        :type folder: str
        :param filename: Output file name
        :type filename: str
        :param fieldnames: List of categories to be saved
        :type fieldnames: list
        :param clear_folder: Whether to empty the folder before saving results
        :type time: bool
        """
        super().__init__(folder, clear_folder)

        self.f = open(filename, 'w')
        self.writer = csv.DictWriter(
            self.f, fieldnames=fieldnames, delimiter=',')
        self.writer.writeheader()

    def __del__(self):
        """Closes the file when the simulation is finished.
        Required for file data to be further used.
        """
        if self.f:
            self.f.close()

    def write(self, row: typing.Dict):
        """Writes data to file.

        :param row: Dictionary of data to be saved
        :type row: dict"""
        self.writer.writerow(row)

#
# Write data in a dict to a csv file
#

import csv
import typing


class _CsvDictWriter:
    def __init__(self, filename: str, fieldnames: typing.List):
        """Initialises a file to store output in, and which categories
        to be record.

        :param filename: Output file name
        :type filename: string
        :param fieldnames: List of categories to be saved
        :type fieldnames: list
        """
        try:
            self.f = open(filename, 'w')
            self.writer = csv.DictWriter(
                self.f, fieldnames=fieldnames, delimiter=',')
            self.writer.writeheader()
        except FileNotFoundError as e:
            self.f = None
            self.writer = None
            # TODO: Log file not found error
            raise e

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

import csv
import typing


class _CsvWriter:
    def __init__(self, filename: str, fieldnames: typing.List):
        """Initialises a file to store output in, and which categories
        to be record.

        :param filename: output file name.
        :type filename: string
        :param fieldnames: list of categories to be saved.
        :type fieldnames: list
        """
        try:
            self.f = open(filename, 'w')
            self.writer = csv.writer(
                self.f, delimiter=',')
            self.writer.writerow(fieldnames)
        except FileNotFoundError as e:
            self.f = None
            self.writer = None
            # TODO: Log file not found error
            print(f"FileNotFoundError: {str(e)}.")
            raise e

    def __del__(self):
        """Closes the file when the simulation is finished.
        Required for file data to be further used.
        """
        if self.f:
            self.f.close()

    def write(self, row: typing.List):
        """Writes data to file.

        :param row: list of data to be saved.
        :type row: list"""
        self.writer.writerow(row)

#
# Write data in a dict to a csv file
#

import csv
import typing
import os
import pandas as pd
import logging

from pyEpiabm.output.abstract_reporter import AbstractReporter


class _CsvDictWriter(AbstractReporter):
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
        self.filename = filename
        self.filepath = os.path.join(folder, filename)
        self.filepath_without_extension = os.path.join(
            folder, os.path.splitext(filename)[0])
        self.fieldnames = fieldnames

        self.f = open(os.path.join(folder, filename), 'w')
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

        Parameters
        ----------
        row : dict
            Dictionary of data to be saved

        """
        self.writer.writerow(row)
        self.f.flush()

    def compress(self):
        """Compresses the csv file and deletes the unzipped csv.
        """
        output_filepath = f"{self.filepath_without_extension}.zip"
        logging.info(f"Zip file created for {self.filename}")
        df = pd.read_csv(self.filepath)
        df.to_csv(output_filepath, index=False, compression={'method': 'zip'})
        self.f.close()
        os.remove(self.filepath)

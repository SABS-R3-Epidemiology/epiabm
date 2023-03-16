#
# AbstractReporter Class
#

import os
import logging


class AbstractReporter:
    """Abstract class for Data Reporters.
    """

    def __init__(self, folder: str, clear_folder: bool = False):
        """Constructor method for reporter. Makes a new folder
        in specified location if one does not already exist.
        Also clears contents of an existing folder if
        clear_folder is true.

        Parameters
        ----------
        folder : str
            Absolute path to folder to store results
        clear_folder : bool
            Whether to empty the folder before saving results

        """
        self.folder = folder
        if os.path.exists(folder):
            if clear_folder:
                try:
                    for file in os.scandir(folder):
                        os.remove(file.path)
                except IsADirectoryError as e:
                    logging.exception(f"{type(e).__name__}: cannot delete"
                                      + f" folder {folder} as it contains"
                                      + " subfolders")

        else:
            os.makedirs(folder)

    def write(self):
        """Write data to .csv files in target folder.

        """
        raise NotImplementedError

#
# AbstractReporter Class
#

import os

from pyEpiabm.core.population import Population


class AbstractReporter:
    """Abstract class for Data Reporters.
    """

    def __init__(self, folder: str, clear_folder: bool):
        """Constructor method for reporter. Makes a new folder
        in specified location if one does not already exist.
        Also clears contents of an existing folder if
        clear_folder is true.

        :param folder: Absolute path to folder to store results
        :type folder: str
        :param clear_folder: Whether to empty the folder before saving results
        :type time: bool
        """
        self.folder = folder
        if os.path.exists(folder):
            if clear_folder:
                try:
                    for file in os.scandir(folder):
                        os.remove(file.path)
                except IsADirectoryError:
                    # TODO - LOG can't clear a folder with subdirectories
                    raise IsADirectoryError("Cannot clear folder as "
                                            + "it is a directory")

        else:
            os.makedirs(folder)

    def __call__(self, population: Population, time: float):
        """Save data from Population at given time in .csv files in target folder.

        :param population: Population: :class:`Population` to output
        :type population: Population
        :param time: Current simulation time
        :type time: float
        """
        raise NotImplementedError

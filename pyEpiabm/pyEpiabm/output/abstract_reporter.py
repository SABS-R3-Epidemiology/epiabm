#
# AbstractReporter Class
#

import os


class AbstractReporter:
    """Abstract class for Data Reporters.
    """

    def __init__(self, folder: str, clear_folder: bool = True):
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

    def write(self):
        """Write data to .csv files in target folder.
        """
        raise NotImplementedError

    def __del__(self):
        """Closes the file when the simulation is finished.
        Required for file data to be further used.
        """
        raise NotImplementedError

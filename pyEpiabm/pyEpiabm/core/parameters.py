#
# Parameters
#

import json
import numpy as np


class Parameters:
    """Class for global parameters.

    Following a singleton Pattern.

    """
    class __Parameters:
        """Singleton Parameters Object.

        """
        def __init__(self, config_file_path):
            """Detailed description of parameters is given
            in github wiki:
            https://github.com/SABS-R3-Epidemiology/epiabm/wiki

            """
            with open(config_file_path, "r") as parameters_file:
                parameters_str = parameters_file.read()
                parameters = json.loads(parameters_str)
                for key, value in parameters.items():
                    if isinstance(value, list):
                        value = np.array(value)
                    setattr(self, key, value)

    _instance = None  # Singleton instance

    @staticmethod
    def instance():
        """Creates singleton instance of __Parameters under
        _instance if one doesn't already exist.

        Returns
        -------
        __Parameters
            An instance of the __Parameters class

        """
        if not Parameters._instance:
            raise RuntimeError("Config file hasn't been set")
        return Parameters._instance

    @staticmethod
    def set_file(file_path):
        """Loads file"""
        Parameters._instance = Parameters.__Parameters(file_path)

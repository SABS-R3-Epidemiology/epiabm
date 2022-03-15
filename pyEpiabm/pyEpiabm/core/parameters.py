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
        def __init__(self):
            """Detailed description of parameters is given
            in github wiki:
            https://github.com/SABS-R3-Epidemiology/epiabm/wiki

            """
            parameters_file = "parameters.json"
            parameters_str = open(parameters_file, "r").read()
            parameters = json.loads(parameters_str)
            for key, value in parameters.items():
                if isinstance(value, list):
                    value = f'np.array({value})'
                exec(f"self.{key} = {value}")

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
            Parameters._instance = Parameters.__Parameters()
        return Parameters._instance

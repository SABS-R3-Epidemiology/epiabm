#
# Parameters
#


class Parameters:
    """Class for global parameters.

    Following a singleton Pattern.
    """
    class __Parameters:
        """Singleton Parameters Object
        """
        def __init__(self):
            pass

    _instance = None  # Singleton instance

    @staticmethod
    def instance():
        """Creates singleton instance of __Parameters under
        _instance if one doesn't already exist.
        """
        if not Parameters._instance:
            Parameters._instance = Parameters.__Parameters()
        return Parameters._instance

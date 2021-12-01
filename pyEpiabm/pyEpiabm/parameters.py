#
# Parameters
#


class Parameters:
    """Class for global parameters
    Singleton Pattern
    """
    class __Parameters:
        """Singleton Parameters Object
        """
        def __init__(self):
            pass

    _instance = None # Singleton instance

    @staticmethod
    def instance():
        """New method
        Creates singleton instance if it doesn't exist
        """
        if not Parameters._instance:
            Parameters._instance = Parameters.__Parameters()
        return Parameters._instance

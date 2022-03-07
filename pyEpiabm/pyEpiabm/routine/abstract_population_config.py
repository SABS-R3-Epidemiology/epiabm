#
# Abstract factory for creation of any population
#


class AbstractPopulationFactory:
    """ Abstract class for population creation.
    """
    @staticmethod
    def make_pop():
        raise NotImplementedError

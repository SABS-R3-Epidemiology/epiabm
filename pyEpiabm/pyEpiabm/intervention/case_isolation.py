#
# Case isolation Class
#

from pyEpiabm.intervention import AbstractIntervention


class CaseIsolation(AbstractIntervention):
    """
    TODO
    """

    def __call__(self):
        for cell in self._population.cells:
            pass

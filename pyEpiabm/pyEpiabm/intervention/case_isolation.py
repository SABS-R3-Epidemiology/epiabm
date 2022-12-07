#
# Case isolation Class
#

from pyEpiabm.intervention import AbstractIntervention


class CaseIsolation(AbstractIntervention):
    """Case isolation intervention
    """

    def __call__(self):
        for cell in self._population.cells:
            for person in cell.persons:
                # Require symptomatic individuals to self-isolate
                person.is_isolating = person.is_symptomatic()

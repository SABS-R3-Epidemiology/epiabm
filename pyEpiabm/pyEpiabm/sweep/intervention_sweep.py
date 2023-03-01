#
# Sweeps for taking care of the interventions
#

from pyEpiabm.core import Parameters
from pyEpiabm.intervention import Vaccination

from .abstract_sweep import AbstractSweep


class InterventionSweep(AbstractSweep):
    """Class to sweep through all possible interventions.
    Check if intervention should take place based on time (and/or threshold).
    Possible interventions:
    vaccination: Implement mass vaccination
    """

    def __init__(self):
        """Call in variables from the parameters file and set flags
        """
        self.interventions = []
        self.intervention_params = Parameters.instance().intervention_params

    def bind_population(self, population):
        self._population = population
        for intervention in self.intervention_params.keys():
            params = self.intervention_params[intervention]
            if intervention == 'vaccine_params':
                self.interventions.append(Vaccination(
                                          population=self._population,
                                          **params,))

    def __call__(self, time):
        """
        Perform interventions that should take place.

        Parameters
        ----------
        time : float
            Simulation time
        """
        for intervention in self.interventions:
            # TODO: better case-count, condition on ICU, etc.
            num_cases = 0
            for cell in self._population.cells:
                for person in cell.persons:
                    if person.is_infectious():
                        num_cases += 1
            if intervention.is_active(time, num_cases):
                intervention(time)

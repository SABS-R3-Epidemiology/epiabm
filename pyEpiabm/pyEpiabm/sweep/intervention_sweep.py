#
# Sweeps for taking care of the interventions
#

from pyEpiabm.core import Parameters
from pyEpiabm.intervention import CaseIsolation, Vaccination, PlaceClosure
from pyEpiabm.intervention import HouseholdQuarantine, SocialDistancing
from pyEpiabm.intervention import DiseaseTesting, TravelIsolation
from .abstract_sweep import AbstractSweep
import warnings


class InterventionSweep(AbstractSweep):
    """Class to sweep through all possible interventions.
    Check if intervention should be active based on policy time and number
    of infected individuals.

    Possible interventions:

            * `case_isolation`: Symptomatic case stays home.
            * `place closure`: Place closure if number of infectious
                               people or icu patients exceeds the threshold.
            * `household quarantine`: Household quarantine if member
                                      is symptomatic.
            * `social distancing`: Social distancing if number of infectious
                                   people exceeds the threshold.
            * `vaccination`: Implement mass vaccination.
            * `disease_testing`: PCR and LFT disease testing.
            * `travel_isolation`: Isolate travelling individuals when
                                  introduced to population.

    """

    def __init__(self):
        """Read in variables from the parameters file

        """
        # Implemented interventions and their activity status
        self.intervention_active_status = {}
        self.intervention_params = Parameters.instance().\
            intervention_params.copy()
        self.intervention_dict = {'case_isolation': CaseIsolation,
                                  'place_closure': PlaceClosure,
                                  'household_quarantine': HouseholdQuarantine,
                                  'social_distancing': SocialDistancing,
                                  'disease_testing': DiseaseTesting,
                                  'vaccine_params': Vaccination,
                                  'travel_isolation': TravelIsolation}

    def bind_population(self, population):
        self._population = population
        for intervention_key, intervention_object in self.\
                intervention_params.items():
            if isinstance(intervention_object, list):
                for index, single_object in enumerate(intervention_object):
                    intervention_init = self.intervention_dict[
                        intervention_key](
                        population=self._population, **single_object)
                    intervention_init.occurrence_index = index
                    self.intervention_active_status[intervention_init] = False

                    # Calculate the current intervention's end date
                    current_end_date = single_object['start_time'] + \
                        [value for key, value in single_object.items() if
                         'delay' in key][0] + \
                        [value for key, value in single_object.items() if
                         'duration' in key][0]

                    # If there are multiple same class of interventions,
                    # initialise it with the first invervention.
                    # Other interventions will be activated and updated
                    # with corrpesonding parameters in the __call__ function
                    if index == 0:
                        Parameters.instance().intervention_params[
                            intervention_key] = single_object
                        previous_end_date = current_end_date

                    # Raise warning message if concurrent interventions occur
                    else:
                        if previous_end_date > single_object['start_time']:
                            warnings.warn(
                                'Concurrent interventions should not occur!')
                    previous_end_date = current_end_date

            else:
                intervention_init = self.intervention_dict[intervention_key](
                            population=self._population, **intervention_object)
                self.intervention_active_status[intervention_init] = False

    def __call__(self, time):
        """Perform interventions that should take place.

        Parameters
        ----------
        time : float
            Simulation time

        """
        for intervention in self.intervention_active_status.keys():
            # TODO:
            # - Include an alternative way of case-count.
            #   Idealy this will be a global parameter that we can plot
            # - Include condition on ICU
            #   Intervention will be activated based on time and cases now.
            #   We would like to implement a threshold based on ICU numbers.
            num_cases = sum(map(lambda cell: cell.number_infectious(),
                            self._population.cells))
            if intervention.is_active(time, num_cases):
                if self.intervention_active_status[intervention] is False:
                    # If the next same type intervention is activated,
                    # update the parameter values with this new intervention
                    # whose values could be retrieved with respect to index
                    if hasattr(intervention, 'occurrence_index'):
                        # Get the intervention type
                        intervention_key = intervention.name
                        # Update parameter values with current
                        # active intervention
                        Parameters.instance().intervention_params[
                            intervention_key] = self.intervention_params[
                            intervention_key][
                            intervention.occurrence_index]
                    self.intervention_active_status[intervention] = True
                intervention(time)

            elif self.intervention_active_status[intervention] is True:
                # turn off intervention
                self.intervention_active_status[intervention] = False
                intervention.turn_off()

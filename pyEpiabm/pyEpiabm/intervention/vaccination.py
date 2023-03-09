#
# Vaccination Class
#

from pyEpiabm.intervention import AbstractIntervention


class Vaccination(AbstractIntervention):
    """Vaccination intervention
    For a description of this intervention see
    https://github.com/SABS-R3-Epidemiology/epiabm/wiki/Interventions#vaccination

    """

    def __init__(
        self,
        daily_doses,
        population,
        **kwargs
    ):
        """ Set the parameters for vaccinations.

        Parameters
        ----------
        daily_doses : int
            Number of vaccine doses administered per day nationwide

        """
        self.daily_doses = daily_doses

        # kwargs read in by this method are: start_time, policy_duration,
        # and case_threshold
        super(Vaccination, self).__init__(**kwargs, population=population)

    def __call__(self, time):
        """ Move down the priority queue removing people and
            vaccinating them.

        Parameters
        ----------
        time : float
            Current simulation time

        """
        number_vaccinated = 0
        while (number_vaccinated < self.daily_doses
                and not self._population.vaccine_queue.empty()):
            person = self._population.vaccine_queue.get()[2]
            person.vaccinate(time)
            number_vaccinated += 1

    def turn_off(self):
        return

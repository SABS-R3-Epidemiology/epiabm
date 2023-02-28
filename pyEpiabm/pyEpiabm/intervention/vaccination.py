#
# Vaccination Class
#

from pyEpiabm.intervention import AbstractIntervention


class Vaccination(AbstractIntervention):
    """Vaccination intervention
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
            Number of vaccine doses administered per day
        """
        self.daily_doses = daily_doses

        # start_time, policy_duration, threshold, population
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
            person.is_vaccinated = True
            person.date_vaccinated = time
            number_vaccinated += 1

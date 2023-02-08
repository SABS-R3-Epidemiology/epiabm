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
        *args,
        **kwargs
    ):
        self.daily_doses = daily_doses

        # start_time, policy_duration, threshold, population
        super(Vaccination, self).__init__(population=population, *args,
                                          **kwargs)

    def __call__(self, time):
        number_vaccinated = 0
        while number_vaccinated < self.vaccines_per_day and not self._population.vaccine_queue.empty():
            person = self._population.vaccine_queue.get()[2]
            person.is_vaccinated = True
            person.date_vaccinated = time
            number_vaccinated += 1
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
        vacc_inf_drop,
	    vacc_susc_drop,
	    time_to_efficacy,
        population,
        *args,
        **kwargs
    ):
        self.vaccines_per_day = daily_doses
        for cell in population.cells:
            for person in cell.persons:
                person.vac_inf_drop = vacc_inf_drop
                person.vac_susc_drop = vacc_susc_drop
                person.time_to_efficacy = time_to_efficacy

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
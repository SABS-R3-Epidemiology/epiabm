#
# Vaccination Class
#

from pyEpiabm.intervention import AbstractIntervention


class Vaccination(AbstractIntervention):
    """Vaccination intervention
    """

    def __init__(
        self,
        vaccine_params,
        population,
        *args,
        **kwargs
    ):
        self.vaccine_start_time = vaccine_params["vaccine_start_time"]
        # self.time_to_next_group = time_to_next_group
        self.vaccines_per_day = vaccine_params["daily_doses"]

        # start_time, policy_duration, threshold, population
        super(Vaccination, self).__init__(population=population, *args,
                                          **kwargs)

    def __call__(self, time):
        if time > self.vaccine_start_time:
            number_vaccinated = 0
            while number_vaccinated < self.vaccines_per_day:
                person = population.vaccine_queue.get()[1]

                person.is_vaccinated = True
                person.date_vaccinated = time
                number_vaccinated += 1

# age prioritised mass vaccination, with vaccination kicking in after 2 weeks. just go for this more simplistic

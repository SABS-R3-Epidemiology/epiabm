#
# Place closure Class
#

from pyEpiabm.intervention import AbstractIntervention


class PlaceClosure(AbstractIntervention):
    """Place closure intervention
    """

    def __init__(
        self,
        closure_duration,
        closure_delay,
        closure_household_infectiousness,
        closure_spatial_params,
        icu_microcell_threshold,
        case_microcell_threshold,
        population,
        *args,
        **kwargs
    ):
        self.closure_duration = closure_duration
        self.closure_delay = closure_delay
        self.icu_microcell_threshold = icu_microcell_threshold
        self.case_microcell_threshold = case_microcell_threshold
        for cell in population.cells:
            for microcell in cell.microcells:
                microcell.closure_household_infectiousness = \
                    closure_household_infectiousness
                microcell.closure_spatial_params = \
                    closure_spatial_params
        # start_time, policy_duration, threshold, population
        super(PlaceClosure, self).__init__(population=population, *args,
                                           **kwargs)

    def __call__(self, time):
        for cell in self._population.cells:
            for microcell in cell.microcells:
                if microcell.closure_start_time is not None:
                    if time > microcell.closure_start_time + self.\
                              closure_duration:
                        # Stop isolating people after their isolation period
                        microcell.closure_start_time = None

                else:
                    if (microcell.count_icu() >= self.
                        icu_microcell_threshold) or \
                            (microcell.count_infectious() >= self.
                                case_microcell_threshold):
                        microcell.closure_start_time = time + self.\
                                                        closure_delay

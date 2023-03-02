#
# Place closure Class
#

from pyEpiabm.intervention import AbstractIntervention


class PlaceClosure(AbstractIntervention):
    """Place closure intervention
    Close specific types of places based on the number of infectious persons
    in their microcells and reopen places after their closure period or
    after the end of the policy.
    """

    def __init__(
        self,
        closure_duration,
        closure_delay,
        case_microcell_threshold,
        population,
        **kwargs
    ):
        self.closure_duration = closure_duration
        self.closure_delay = closure_delay
        self.case_microcell_threshold = case_microcell_threshold
        super(PlaceClosure, self).__init__(population=population,
                                           **kwargs)

    def __call__(self, time):
        for cell in self._population.cells:
            for microcell in cell.microcells:
                if (hasattr(microcell, 'closure_start_time')) and (
                        microcell.closure_start_time is not None):
                    if time > microcell.closure_start_time + self.\
                              closure_duration:
                        # Reopen places after their closure period
                        microcell.closure_start_time = None
                else:
                    if (microcell.count_infectious() >= self.
                            case_microcell_threshold):
                        microcell.closure_start_time = time + self.\
                                                        closure_delay

    def turn_off(self):
        for cell in self._population.cells:
            for microcell in cell.microcells:
                if (hasattr(microcell, 'closure_start_time')) and (
                        microcell.closure_start_time is not None):
                    microcell.closure_start_time = None

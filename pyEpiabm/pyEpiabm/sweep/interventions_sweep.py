#
# Sweeps for taking care of the interventions
#

from pyEpiabm.core import Parameters, Person, Population
from .abstract_sweep import AbstractSweep

class InterventionsSweep(AbstractSweep):
    """Class to sweep through all possible interventions. 
    Check if intervention should take place based on time (and/or threshold).
    Possible interventions:
    isolate_individual: Symptomatic case stays home.
    """

    def __init__(self):
        """Call in variables from the parameters file and set flags
        """
        self.interventions = []
        self.intervention_params = Parameters.instance().intervention_params       #{'case_isolation': [time_start, duration]}
        for intervention in self.intervention_params.keys():
            params = self.intervention_params[intervention]
            if intervention == 'case_isolation':
                self.interventions.append(CaseIsolation(*params))

    def __call__(self, time):
        """
        Call the trigger function to set flag for all interventions.
        Perform interventions that should take place.

        Parameters
        ----------
        time : float
            Simulation time
        """
        #change this to class setup
        self.trigger_interventions()
        if self.flag_CI == True:
            self.case_isolation()
        

    #NTH: loop through all people in population and update their parameters

    def trigger_interventions(self, time):
        """Check if intervention is triggered
        """
        #check time start, time duration, and/or threshold. 
        for intervention in self.intervention_params.keys():
            if self.intervention_params[intervention][0] <= time: #current time bigger or equal to intervention start time
                # self.intervention_flags[intervention] = True
                if intervention == 'case_isolation':
                    self.flag_CI = True
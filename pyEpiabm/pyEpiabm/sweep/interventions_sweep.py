#
# Sweeps for taking care of the interventions
#

from pyEpiabm.core import Parameters, Person, Population

from .abstract_sweep import AbstractSweep

class InterventionsSweep():
    """Class to sweep through all the interventions
    """

    def __init__(self):
        """Call in variables from the parameters file and set flags
        """
        intervention_params = Parameters.instance().intervention_params


    def __call__(self, time):
        """

        Parameters
        ----------
        time : float
            Simulation time
        """

    #call the trigger function 
    #NTH: loop through all people in population and update their parameters

        

    def trigger_interventions(self):
        """Check if intervention is triggered
        """
        #check time start, time duration, and/or threshold. 

        pass

    def isolate_individual(self):
        pass
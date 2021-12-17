#
# Sweep to update people present in a place
#
import random
import numpy as np
from .abstract_sweep import AbstractSweep


class UpdatePlaceSweep(AbstractSweep):
    """Class to update people in the "Place"
    class.
    """
    def __call__(self, time: int):
        """Given a population structure, updates the people
        present in each place at a specific timepoint.

        :param time: Current simulation time
        :type time: int
        """
        # Double loop over the whole population, clearing places
        # and refilling them.
        for cell in self._population.cells:
            for place in cell.places:
                place.empty_place()
                # Possibly want to later differentiate between
                # the fixed population of a place ie staff, and
                # the variable population ie customers.

                # Ensure that the number of people put in the place
                # is at most its capacity or the total number of
                # people in the microcell.
                max_capacity = np.minimum(place.max_capacity,
                                          len(place.microcell.persons))

                new_capacity = random.randint(1, max_capacity)
                for _ in range(new_capacity):
                    i = random.randint(1, len(place.microcell.persons))
                    place.add_person(place.microcell.persons[i-1])

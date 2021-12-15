from .abstract_sweep import AbstractSweep
import random
import numpy as np


class UpdatePlaceSweep(AbstractSweep):
    """Class to update people in the "Place"
    class.
    """
    def __call__(self, time: int):
        """Given a population structure, updates the people
        present in each place at a specific timepoint.

        :param time: current simulation time.
        :type time: int
        """
        # Double loop over the whole population, clearing places
        # and refilling them.
        for cell in self._population.cells:
            for place in cell.places:
                place.empty_place()
                # Possibly want to later differentiate between
                # the fixed population of a place ie staff, and
                # the variable population.

                # Ensure that we don't put more people than live in
                # the microcell.
                max_capacity = np.minimum(place.max_capacity,
                                          len(place.microcell.persons))
                # what if there aren't enough in microcell
                new_capacity = random.randint(1, max_capacity)
                for _ in range(new_capacity):
                    i = random.randint(1, len(place.microcell.persons))
                    place.add_person(place.microcell.persons[i-1])

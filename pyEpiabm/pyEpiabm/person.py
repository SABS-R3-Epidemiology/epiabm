#
# Person Class
#


class Person:
    """Class to represent each person in a population.

    :param microcell: An instance of an :class:`Microcell`.
    :type microcell: Microcell
    """

    def __init__(self, microcell):
        """Constructor Method.

        :param microcell: Person's parent :class:`Microcell` instance.
        :type microcell: Microcell
        """
        self.age = 0
        self.susceptibility = 0
        self.infectiveness = 0
        self.microcell = microcell

    def __repr__(self):
        """String Representation of Person.

        :return: String representation of person
        :rtype: str
        """
        return f"Person, Age = {self.age}"

from pyEpiabm.output._csv_writer import _CsvWriter
from pyEpiabm.core import Population


class AgeStratifiedNewCasesWriter(_CsvWriter):
    """ Writer for collecting number of daily new cases
        and splitting them between age groups
    """

    def __init__(self, folder: str):
        """ Constructor method

        Parameters
        ----------
        folder : str
            Absolute path to folder to store results
        """
        super().__init__(
            folder, 'age_stratified_new_cases.csv',
            ['t', 'cell', 'age_group', 'new_cases'], False)

    def write(self, t: float, population: Population):
        """ Write method
        Write daily new cases spit by age group in
        population to file

        Parameters
        ----------
        t : float
            Current simulation time
        population : Population
            Population to record
        """
        for cell in population.cells:
            new_cases = {}
            for person in cell.persons:
                if person.infection_start_time is not None and \
                   person.infection_start_time > (t-1):
                    if person.age_group in new_cases:
                        new_cases[person.age_group] += 1
                    else:
                        new_cases[person.age_group] = 1
            for age_group, cases in new_cases.items():
                super().write([t, cell.id, age_group, cases])

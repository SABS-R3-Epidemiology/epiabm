from pyEpiabm.output._csv_writer import _CsvWriter
from pyEpiabm.core import Population


class NewCasesWriter(_CsvWriter):
    """ Writer for collecting number of daily new cases
    """

    def __init__(self, folder: str):
        """ Constructor method

        Parameters
        ----------
        folder : str
            Absolute path to folder to store results
        """
        super().__init__(
            folder, 'new_cases.csv',
            ['t', 'cell', 'new_cases'], False)

    def write(self, t: float, population: Population):
        """ Write method
        Write daily new cases from population to file

        Parameters
        ----------
        t : float
            Current simulation time
        population : Population
            Population to record
        """
        for cell in population.cells:
            new_cases = 0
            for person in cell.persons:
                if person.infection_start_times != [] and \
                   person.infection_start_times[-1] > (t-1):
                    new_cases += 1
            super().write([t, cell.id, new_cases])

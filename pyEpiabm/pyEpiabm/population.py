import pyEpiabm as pe


class Population:
    def __init__(self):
        self.cells = []

    def info(self):
        return "Population, {} cells.".format(len(self.cells))

    def add_cells(self, n):
        for i in range(n):
            self.cells.append(pe.Cell())

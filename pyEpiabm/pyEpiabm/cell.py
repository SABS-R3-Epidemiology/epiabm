import pyEpiabm as pe


class Cell:
    def __init__(self):
        self.microcells = []
        self.people = []

    def info(self):
        return "Cell, {} microcells, {} people.".format(len(self.microcells),
                                                        len(self.people))

    def add_microcells(self, n):
        for i in range(n):
            self.microcells.append(pe.Microcell(self))

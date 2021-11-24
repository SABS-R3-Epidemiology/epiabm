import pyEpiabm as pe


class Microcell:
    def __init__(self, cell):
        self.people = []
        self.cell = cell

    def info(self):
        return "Microcell, {} people".format(len(self.people))

    def add_people(self, n):
        for i in range(n):
            p = pe.Person(self)
            self.cell.people.append(p)
            self.people.append(p)

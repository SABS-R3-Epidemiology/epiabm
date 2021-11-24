

class Population:
    def __init__(self):
        self.cells = []

    def info(self):
        return "Population, {} cells.".format(len(self.cells))

class Cell:
    def __init__(self):
        self.microcells = []
        self.people = []
    
    def info(self):
        return "Cell, {} microcels, {} people.".format(len(self.microcells), len(self.people))

class Microcell:
    def __init__(self, cell):
        self.people = []
        self.cell = cell
    
    def info(self):
        return "Microcell, {} people".format(len(self.people))

class Person:
    def __init__(self, microcell):
        self.age = 0
        self.susceptibility = 0
        self.infectiveness = 0
        self.microcell = microcell
    
    def info(self):
        return "Person."


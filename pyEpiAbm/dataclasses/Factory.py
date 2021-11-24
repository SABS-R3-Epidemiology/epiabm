from .Population import *

class Factory:
    def makePopulation(self):
        return Population()

    def addCells(self, population, n):
        for i in range(n):
            population.cells.append(Cell())

    def addMicrocells(self, cell, n):
        for i in range(n):
            cell.microcells.append(Microcell(cell))
    
    def addPeople(self, microcell, n):
        for i in range(n):
            p = Person(microcell)
            microcell.cell.people.append(p)
            microcell.people.append(p)

    
class Population:
    def __init__(self):
        self.cells = []

    def info(self):
        return "Population, {} cells.".format(len(self.cells))

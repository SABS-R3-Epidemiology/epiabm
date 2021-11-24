class Microcell:
    def __init__(self, cell):
        self.people = []
        self.cell = cell
    
    def info(self):
        return "Microcell, {} people".format(len(self.people))
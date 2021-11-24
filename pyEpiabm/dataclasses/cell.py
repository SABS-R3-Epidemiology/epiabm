class Cell:
    def __init__(self):
        self.microcells = []
        self.people = []
    
    def info(self):
        return "Cell, {} microcels, {} people.".format(len(self.microcells), len(self.people))
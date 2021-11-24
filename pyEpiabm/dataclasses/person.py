class Person:
    def __init__(self, microcell):
        self.age = 0
        self.susceptibility = 0
        self.infectiveness = 0
        self.microcell = microcell
    
    def info(self):
        return "Person."

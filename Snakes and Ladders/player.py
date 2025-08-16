class Player:
    def __init__(self, name):
        self.name = name
        self.pos = 0

    def get_name(self):
        return self.name
    
    def get_pos(self):
        return self.pos
    
    def set_pos(self, pos):
        self.pos = pos
    
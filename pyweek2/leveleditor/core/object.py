class GameObject:
    def __init__(self,name=None,sprite=None):
        self.name = name
        self.sprite = sprite
    def __repr__(self):
        return self.name

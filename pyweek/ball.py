from constants import CODE # Michal's UgLy hack. :)

class Ball:
    def __init__(self, room, position):
        self.room = room
        self.radius = HERO.RADIUS
        self.geom = self.room.addBlock(position, 2*self.radius, 2*self.radius)
        self.geom.code = CODE.BALL

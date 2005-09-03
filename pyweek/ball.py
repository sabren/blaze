from constants import CODE # Michal's UgLy hack. :)

class Ball:
    def __init__(self):
        self.geom = ode.GeomSphere(space=None, radius=HERO.RADIUS)
        self.geom.code = CODE.BALL

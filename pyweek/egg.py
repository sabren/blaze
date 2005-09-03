from constants import CODE # Michal's UgLy hack. :)

class Egg:
    def __init__(self):
        self.geom = ode.GeomSphere(space=None, radius=HERO.RADIUS)
        self.geom.code = CODE.FOOD

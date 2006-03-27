import pygame, eventnet.driver, sprites, cPickle

class tile(sprites.Sprite):
    def __init__(self, image, pos=(0,0), solid=False):
        sprites.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.move(pos)
        self.solid = solid

    def set_pos(self, pos):
        self.rect.move(pos)

default_tile = tile(pygame.image.load(
    os.path.join('data', 'tiles', 'blue.bmp')))
empty_level={'enemies': [], 'hero': (0,0), 'tiles'=[[default_tile]]}

class level:
    '''
    A group to manage level tiles.
    '''
    def __init__(self, source=empty_level):
        self.tiles = sprites.Group()
        self.sprites = sprites.Group(source['enemies'])
        self.background = pygame.Surface(
            (len(source['tiles']), len(source['tiles'][0])))
        for row in range(len(source['tiles'])):
            for tile in row:
                self.tiles.add(tile)
        self.tiles.draw(self.background)
        self.hero = sprites.hero(source['pos'], self.sprites)
        self.level = self.background.copy()

    def tick(self):
        self.sprites.update()
        self.sprites.draw(self.level)
        self.sprites.clear(self.level, self.background)

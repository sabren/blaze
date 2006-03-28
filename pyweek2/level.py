import pygame, eventnet.driver, sprites, cPickle, os, glob

class tile(sprites.Sprite):
    def __init__(self, image, solid=False):
        self.image = pygame.image.load(image)
        sprites.Sprite.__init__(self, self.image)
        self.rect = self.image.get_rect()
        self.solid = solid

default_tile = tile(os.path.join('data', 'tiles', 'blue.bmp'))
reg_tiles = [tile(x) for x in glob.glob(os.path.join('data', 'tiles', '*.bmp'))]
solid_tiles = [tile(x, True) for x in glob.glob(os.path.join('data', 'tiles',
                                                             'solid', '*.bmp'))]
tiles = solid_tiles + reg_tiles
test_tiles = [
    solid_tiles,
    solid_tiles,
    solid_tiles,
    solid_tiles
    ]
empty_level={'enemies': [], 'hero': (0,0), 'tiles': test_tiles}

class level:
    '''
    A group to manage levels.
    '''

    def __init__(self, source=empty_level):
        self.tiles = sprites.Group()
        self.sprites = sprites.Group(source['enemies'])
        self.background = pygame.Surface((len(source['tiles'])*50,
                                          len(source['tiles'][0])*50))
        y = 0
        for row in source['tiles']:
            x = 0
            for tile in row:
                self.background.blit(tile.image, (x,y))
                self.tiles.add(tile)
                x += 50
            y += 50
        self.tiles.draw(self.background)
        self.hero = sprites.hero(source['hero'], [self.sprites])
        self.level = self.background.copy()

    def tick(self):
        self.sprites.update()
        self.sprites.draw(self.level)
        self.sprites.clear(self.level, self.background)

if __name__=='__main__':
    lvl = level()
    lvl.tick()
    pygame.display.set_mode((800, 600)).blit(lvl.background, (0,0))
    pygame.display.flip()
    pygame.time.wait(5000)

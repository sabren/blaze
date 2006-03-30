import pygame, eventnet.driver, sprites, cPickle, os, glob

try:
    tmpfile = os.path.join(os.environ['TMP'], 'temp.bmp')
except KeyError, e:
    tmpfile = 'temp.bmp' #defaulting to CWD doesn't seem nice, but...

class tile(sprites.Sprite):
    def __init__(self, image, solid=False):
        sprites.Sprite.__init__(self, image)
        self.image = image
        self.rect = self.image.get_rect()
        self.solid = solid

default_tile = tile(pygame.image.load(os.path.join(
    'data', 'tiles', 'water.bmp')))
reg_tiles = [tile(pygame.image.load(x)) for x in glob.glob(
    os.path.join('data', 'tiles', '*.bmp'))]
solid_tiles = [tile(pygame.image.load(x), True) for x in glob.glob(
    os.path.join('data', 'tiles', 'solid', '*.bmp'))]
tiles = solid_tiles + reg_tiles
test_tiles = [tiles, tiles, tiles, tiles]
empty_level={'enemies': [], 'hero': (0,0), 'tiles': test_tiles}

def load(name):
    '''
    This and save() convert pygame surfaces to strings through a tempfile so
    that the surfaces can be pickled.
    '''

    f = open(os.path.join('data', 'levels', name+'.lvl'))
    lvl = cPickle.load(f)
    f.close()
    for i in range(len(lvl['enemies'])):
        enemy = lvl['enemies'][i]
        del(lvl['enemies'][i])
        f = open(tmpfile, 'wb')
        f.write(enemy[0])
        f.close()
        enemy = sprites.Sprite(pygame.image.load(tmpfile), pos=enemy[1])
        lvl['enemies'].insert(i, enemy)
    for index in range(len(lvl['tiles'])):
        row = lvl['tiles'][index]
        del(lvl['tiles'][index])
        for i in range(len(row)):
            t = row[i]
            del(row[i])
            f = open(tmpfile, 'wb')
            f.write(t[0])
            f.close()
            t = tile(pygame.image.load(tmpfile), t[1])
            row.insert(i, t)
        lvl['tiles'].insert(index, row)

    return lvl

def save(name, lvl):
    '''
    The ugliest code in the program as of today :p see load()
    '''

    for i in range(len(lvl['enemies'])):
        enemy = lvl['enemies'][i]
        rect = enemy.rect
        del(lvl['enemies'][i])
        enemy = sprites.Sprite(enemy.image, pos=enemy.rect.topleft)
        enemy.rect = rect
        pygame.image.save(enemy.image, tmpfile)
        enemy.image = open(tmpfile, 'rb').read()
        enemy = (enemy.image, enemy.solid)
        lvl['enemies'].insert(i, enemy)

    for index in range(len(lvl['tiles'])):
        row = lvl['tiles'][index]
        del(lvl['tiles'][index])
        for i in range(len(row)):
            t = row[i]
            rect = t.rect
            del(row[i])
            t = tile(t.image, t.solid)
            t.rect = rect
            pygame.image.save(t.image, tmpfile)
            t.image = open(tmpfile, 'rb').read()
            t = (t.image, t.solid)
            row.insert(i, t)
        lvl['tiles'].insert(index, row)

    cPickle.dump(lvl, open(os.path.join('data', 'levels', name+'.lvl'), 'w'))

def new(width, height):
    tiles = []
    for row in range(height):
        y = row
        row = []
        for Tile in range(width):
            x = Tile
            Tile = tile(default_tile.image, default_tile.solid)
            Tile.rect = Tile.rect.move((x,y))
            row += [Tile]
        tiles += [row]
    return {'enemies': [], 'hero': (0,0), 'tiles': tiles}

class level:
    '''
    A class to manage levels. Prob'ly should have (and pyob'ly will) do
    all this in gamestate.
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
                tile.rect = tile.rect.move((x,y))
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
    for row in new(2,5)['tiles']:
        print row

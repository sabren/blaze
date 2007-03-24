import pygame
from directicus.gfx import loadGrid,Animation

if not pygame.display.get_surface():
    pygame.display.set_mode((800,600),pygame.HWSURFACE)

class ResourceManager(object):
    class Ranger:
        still = pygame.image.load('data/ranger.png').convert()
        walk = dict()
        walkMap = loadGrid(pygame.image.load('data/animations/walk.png').convert(),(35,60))
        angles = ['0','45','90','135','180','225','270','335']
        for angle in angles:
            walk[angle] = Animation(walkMap[angles.index(angle)],True)

    class Arrow:
        still = pygame.image.load('data/arrow.png').convert()

    class Tree:
        still = pygame.image.load('data/tree.png').convert()

    class Castle:
        still = pygame.image.load('data/castle.png').convert()
        small = pygame.image.load('data/castle-small.png').convert()

    class Grass:
        still = pygame.image.load('data/grass.png').convert()

    class Cursor:
        sword = pygame.image.load('data/cursors/sword.png').convert()

    __all__ = ['Ranger','Tree','Castle','Grass','Cursor']

class Ranger:
    still = pygame.image.load('data/ranger.png').convert()
    walk = dict()
    walkMap = loadGrid(pygame.image.load('data/animations/walk.png').convert(),(35,60))
    angles = ['0','45','90','135','180','225','270','335']
    for angle in angles:
        walk[angle] = Animation(walkMap[angles.index(angle)],True)

class Tree:
    still = pygame.image.load('data/tree.png').convert()

class Castle:
    still = pygame.image.load('data/castle.png').convert()
    small = pygame.image.load('data/castle-small.png').convert()

class Grass:
    still = pygame.image.load('data/grass.png').convert()

class Cursor:
    sword = pygame.image.load('data/cursors/sword.png').convert()

class Arrow:
    images = loadGrid(pygame.image.load('data/arrow.png').convert(),(30,30))

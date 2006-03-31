'''
Script to generate dummy image files for use until we have some real graphics.
'''

import pygame, os, time
pygame.init()

def create_dummies():
    #dummy tiles (filled with different colors)
    dummy_colors = [('red', (255,0,0)),
                    ('green', (0,255,0)),
                    ('black', (0,0,0)),
                    ('white', (255,255,255)),
                    ('gray', (115,115,115))]
    dummy_tile = pygame.Surface((50, 50))
    for color in dummy_colors:
        dummy_tile.fill(color[1])
        pygame.image.save(dummy_tile, os.path.join('tiles', 'solid',
                                                   '%s.bmp' % color[0]))
    dummy_tile.fill((0,0,255))
    pygame.image.save(dummy_tile, os.path.join('tiles', 'blue.bmp'))

if __name__=='__main__':
    create_dummies()

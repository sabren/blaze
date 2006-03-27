'''
Script to generate dummy image files for use until we have some real graphics.
'''

import pygame, os, time
pygame.init()

def create_dummies():

    #dummy tiles (filled with different colors)
    dummy_colors = [('blue', (0,0,255)),
                    ('red', (255,0,0)),
                    ('green', (0,255,0)),
                    ('black', (0,0,0)),
                    ('white', (255,255,255)),
                    ('gray', (115,115,115))]
    dummy_tile = pygame.Surface((50, 50))
    for color in dummy_colors:
        dummy_tile.fill(color[1])
        pygame.image.save(dummy_tile, os.path.join('tiles',
                                                   '%s.bmp' % color[0]))

    #hero images
    hull = pygame.Surface((50,100))
    hull.fill((255,255,255))
    pygame.draw.polygon(hull, (115,115,115), [(0,100),(50,100),(25,0)])
    pygame.image.save(hull, os.path.join('hero', 'hull.bmp'))

    turret = pygame.surface.Surface((50,50))
    turret.fill((255,255,255,0))
    pygame.draw.line(turret, (0,0,0), (25,25), (25,5), 3)
    pygame.draw.circle(turret, (95,95,95), (25,25), 10)
    pygame.image.save(turret, os.path.join('hero', 'turret.bmp'))

    #cannon ball
    shell = pygame.Surface((20,20))
    shell.fill((255,255,255,0))
    pygame.draw.circle(shell, (0,0,0), (10,10), 5)
    pygame.image.save(shell, 'shell.bmp')
    

if __name__=='__main__':
    create_dummies()

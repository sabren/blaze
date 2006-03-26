'''
Script to generate dummy image files for use until we have some real graphics.
'''

import pygame, os
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
    hero = pygame.Surface((50,100))
    hero.fill((255,255,255))
    pygame.draw.rect(hero, (115,115,115), hero.get_rect())
    for angle in range(100):
        angle = angle*(360.0/100.0)
        pygame.image.save(pygame.transform.rotate(hero, angle),
                          os.path.join('hero', 'hull', '%s.bmp' % angle))

if __name__=='__main__':
    create_dummies()

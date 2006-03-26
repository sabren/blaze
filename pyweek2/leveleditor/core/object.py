import pygame

class GameObject:
    def __init__(self,name=None,sprite=None):
        self.name = name
        self.sprite = sprite
        self.font = pygame.font.SysFont('Arial', 11)
    def render(self,screen,toolbar_rect,x,y):
        img = self.font.render(self.name, True, (255,255,255))
        x = (toolbar_rect.width/2)-(img.get_width()/2)
        screen.blit(img, (x,y))
        y += img.get_height()+5
        pygame.display.flip()
        return [x,y]
    def __repr__(self):
        return self.name

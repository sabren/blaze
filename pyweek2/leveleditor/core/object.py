import pygame, os

class GameObject:
    def __init__(self,name=None,sprite=None,group=None):
        self.name = name
        self.sprite = sprite
        self.group = group
        self.font = pygame.font.SysFont('Arial', 11)
    def render(self,screen,toolbar_rect,x,y,sprite):
        if os.path.exists(sprite):
            icon = pygame.image.load(sprite).convert()
            x = (toolbar_rect.width/2)-(icon.get_width()/2)
            screen.blit(icon, (x,y))
            y += icon.get_height()+5            
        img = self.font.render(self.name, True, (255,255,255))
        x = (toolbar_rect.width/2)-(img.get_width()/2)
        screen.blit(img, (x,y))
        y += img.get_height()+5
        pygame.display.flip()
        return [x,y,img.get_width(),img.get_height()]
    def __repr__(self):
        return self.names

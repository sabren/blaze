import pygame, os, sys

class GameObject:
    def __init__(self,name=None,sprite=None,group=None):
        self.name = name
        self.sprite = sprite
        self.group = group
        self.font = pygame.font.SysFont('Arial', 11)
        self.text_position = None
        self.text_size = None
        self.image_position = None
        self.image_size = None
        self.highlighted = False
    
    def highlight(self,screen):
        if not self.highlighted:
            self.highlighted = True
            img = self.font.render(self.name, True, (255,0,0))
            screen.fill((255,255,255),pygame.Rect(self.text_position[0],self.text_position[1],img.get_width(),img.get_height()))
            screen.blit(img, self.text_position)

    def unhighlight(self,screen):
        if self.highlighted:
            img = self.font.render(self.name, True, (0,0,0))
            screen.fill((255,255,255),pygame.Rect(self.text_position[0],self.text_position[1],img.get_width(),img.get_height()))
            screen.blit(img, self.text_position)        
            self.highlighted = False
        
    def render(self,screen,toolbar_rect,x,y,sprite):
        if os.path.exists(sprite):
            icon = pygame.image.load(sprite).convert()
            x = (toolbar_rect.width/2)-(icon.get_width()/2)
            screen.blit(icon, (x,y))
            self.image_position = (x,y)
            y += icon.get_height()+5            
            self.image_size = (icon.get_width(),icon.get_height())
        img = self.font.render(self.name, True, (0,0,0))
        x = (toolbar_rect.width/2)-(img.get_width()/2)
        screen.blit(img, (x,y))
        self.text_position = (x,y)
        y += img.get_height()+5
        self.image_size = (img.get_width(),img.get_height())
        return [x,y]
    
    def get_size_part(self,index):
        """
        Get either the width or height of the object
        index = 1 => height
        index = 0 => width
        """
        w1 = 0
        w2 = 0
        if not self.image_size is None:
            w1 = self.image_size[index]
        if not self.text_size is None:
            w2 = self.text_size[index]
        if w1 > w2: return w1
        else: return w2
        
    def get_width(self): return self.get_size_part(0)
    def get_height(self): return self.get_size_part(1)
    
    def get_top_left_part(self,index):
        """
        Get either the top or left of the object
        index = 1 => top (y)
        index = 0 => left (x)
        """
        t1 = sys.maxint
        t2 = sys.maxint
        final = sys.maxint
        if not self.image_position is None:
            t1 = self.image_position[index]
        if not self.text_position is None:
            t2 = self.text_position[index]
        if t1 < t2: final = t1
        else: final = t2
        if final == sys.maxint: return None
        return final
    
    def get_left(self): return self.get_top_left_part(0)
    def get_top(self): return self.get_top_left_part(1)
    
    def get_top_left(self):
        top = self.get_top()
        left = self.get_left()
        if not top is None and not left is None:
            return [left,top]
        else:
            raise Exception("Cannot get top left of an object which hasn't been rendered yet")
    
    def __repr__(self):
        return self.name

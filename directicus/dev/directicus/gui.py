# Directicus
# Copyright (C) 2006-2007 Team Trailblazer

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import pygame,directicus

if not pygame.font.get_init():
    pygame.font.init()

__all__=['BOLD','ITALIC','UNDERLINE','NORMAL','LEFT','RIGHT','CENTER','TOP','BOTTOM',
         'REPEAT','REPEAT_X','REPEAT_Y','NO_REPEAT','Element']

# Font styles
BOLD = 'bold'
ITALIC = 'italic'
UNDERLINE = 'underline'
NORMAL = 'normal'

# Alignment
LEFT = 'left'
RIGHT = 'right'
CENTER = 'center'
TOP = 'top'
BOTTOM = 'bottom'

# Background repeat
REPEAT = 'repeat'
REPEAT_X = 'repeat-x'
REPEAT_Y = 'repeat-y'
NO_REPEAT = 'no-repeat'

STYLING = ['color',
           'font_size',
           'font',
           'font_style',
           'pos',
           'align',
           'valign',
           'background_color',
           'background_image',
           'background_style',
           'size',
           'border_top',
           'border_left',
           'border_right',
           'border_bottom',
           'padding',
        ]

class Element(directicus.sprite.Sprite,directicus.event.Listener):
    color = (0,0,0)
    font_size = 12
    font = 'Verdana'
    _font = None
    font_style = NORMAL
    text = ''
    align = LEFT
    valign = TOP
    pos = (0,0)
    size = (1,1)
    background_color = None
    background_image = None
    background_style = REPEAT
    children = None
    _children = None
    parent = None
    _mouseOver = False
    border_top = None
    border_left = None
    border_right = None
    border_bottom = None
    padding = 0
    
    __all__ = STYLING + [
       'text',
       'children',
       'parent',
       'update',
       'rect'
       ]
    
    def __init__(self,*children,**kwargs):
        self.__dict__.update(**kwargs)
        self.children = list(children)
        for child in self.children:
            if type(child) == type('<string>'):
                i = self.children.index(child)
                child = Element(text=child)
                self.children[i] = child
            child.parent = self
        self._children = pygame.sprite.Group(self.children)
        self.update()
        directicus.event.Listener.__init__(self)
        directicus.sprite.Sprite.__init__(self)
        
    def onKeyDown(self,event):
        pass
    
    def onKeyUp(self,event):
        pass
    
    def onMouseButtonDown(self,event):
        event = directicus.event.Event(event.type,**event.kwargs)
        event.pos = list(event.pos)
        parents = []
        elem = self.parent
        while elem:
            parents.append(elem)
            elem = elem.parent
        parents.reverse()
        for parent in parents:
            event.pos[0] -= parent.rect.x
            event.pos[1] -= parent.rect.y
        if self.rect.collidepoint(*event.pos):
            self.onMouseDown(event)
        
    def onMouseButtonUp(self,event):
        event = directicus.event.Event(event.type,**event.kwargs)
        event.pos = list(event.pos)
        parents = []
        elem = self.parent
        while elem:
            parents.append(elem)
            elem = elem.parent
        parents.reverse()
        for parent in parents:
            event.pos[0] -= parent.rect.x
            event.pos[1] -= parent.rect.y
        if self.rect.collidepoint(*event.pos):
            self.onMouseUp(event)
        
    def onMouseDown(self,event):
        pass
    
    def onMouseUp(self,event):
        pass
        
    def onMouseMotion(self,event):
        event = directicus.event.Event(event.type,**event.kwargs)
        event.pos = list(event.pos)
        parents = [self]
        elem = self.parent
        while elem:
            parents.append(elem)
            elem = elem.parent
        parents.reverse()
        for parent in parents:
            event.pos[0] -= parent.rect.x
            event.pos[1] -= parent.rect.y
        if self.rect.collidepoint(*event.pos):
            self.onMouseOver(event)
        elif self._mouseOver:
            self.onMouseOut(event)
            
    def onMouseOver(self,event):
        self._mouseOver = True
        
    def onMouseOut(self,event):
        self._mouseOver = False
        
    def update(self):
        self._font = pygame.font.SysFont(self.font,self.font_size)
        if UNDERLINE in self.font_style:
            self._font.set_underline(True)
        else:
            self._font.set_underline(False)
        if BOLD in self.font_style:
            self._font.set_bold(True)
        else:
            self._font.set_bold(False)
        if ITALIC in self.font_style:
            self._font.set_italic(True)
        else:
            self._font.set_italic(False)
        if self.text:
            image = self._font.render(self.text,True,self.color)
            self.setBackground(image)
        else:
            self.image = pygame.Surface(self.size)
            if self.background_image:
                self.setBackground()
            elif self.background_color:
                self.image.fill(self.background_color)
        self.rect = self.image.get_rect()
        if self.text:
            self.size = self.rect.size
        if self.align == LEFT:
            self.rect.left = self.pos[0]
        elif self.align == CENTER:
            self.rect.centerx = self.pos[0]
        elif self.align == RIGHT:
            self.rect.right = self.pos[0]
        if self.valign == TOP:
            self.rect.top = self.pos[1]
        elif self.valign == CENTER:
            self.rect.centery = self.pos[1]
        elif self.valign == BOTTOM:
            self.rect.bottom = self.pos[1]
        if self.border_top != None:
            pygame.draw.line(
                self.image,
                self.border_top[0],
                (0,0),
                (self.image.get_width(),0),
                self.border_top[1])
        if self.border_left != None:
            pygame.draw.line(
                self.image,
                self.border_left[0],
                (0,0),
                (0,self.image.get_height()),
                self.border_left[1])
        if self.border_right != None:
            pygame.draw.line(
                self.image,
                self.border_right[0],
                (self.image.get_width()-self.border_right[1],0),
                (self.image.get_width()-self.border_right[1],self.image.get_height()),
                self.border_right[1])
        if self.border_bottom != None:
            pygame.draw.line(
                self.image,
                self.border_bottom[0],
                (0,self.image.get_height()-self.border_bottom[1]),
                (self.image.get_width()-self.border_bottom[1],
                 self.image.get_height()-self.border_bottom[1]),
                self.border_bottom[1])

        self._children.update()
        self._children.draw(self.image)
            
    def setBackground(self,image=None):
        if not hasattr(self,'image'):
            self.image = pygame.Surface(self.size)
            self.image.fill((0,100,255))
            self.image.set_colorkey(self.image.get_at((0,0)))
        background = self.image.copy()
        if self.background_style:
            if self.background_color:
                background.fill(self.background_color)
            if self.background_image:
                background.blit(self.background_image,(0,0))
            tile = background.copy()
        if self.background_image:
            if self.background_style in (REPEAT,REPEAT_X):
                for col in range((background.get_width()/self.background_image.get_width())+1):
                    background.blit(tile,(col*self.background_image.get_width(),0))
            if self.background_style in (REPEAT,REPEAT_Y):
                tile = background.copy()
                for row in range((background.get_height()/self.background_image.get_height())+1):
                    background.blit(tile,(0,row*self.background_image.get_height()))
        if image:
            background.blit(image,(0,0))
        self.image = background
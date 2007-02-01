import pygame

def saveGrid(map,filename):
    '''
    Saves a series of images into a single file (like frames in an animation).
    '''

    height = map[0][0].get_height()
    width = map[0][0].get_width()
    new = pygame.Surface((width*len(map[0]),(height*len(map))))
    alpha = map[0][0].get_colorkey()
    if alpha:
        new.fill(alpha)
        new.set_colorkey(alpha)
    y = 0
    for row in map:
        x = 0
        for image in row:
            new.blit(image, (x,y))
            x += width
        y += height
    pygame.image.save(new,filename)

def loadGrid(image,size=(20,20),colorkey=None):
    '''
    Inverse of saveGrid.
    '''

    if type(image) == type('<string>'):
        image = pygame.image.load(image)

    map = []
    y = 0
    for row in range(image.get_height()/size[1]):
        row = []
        x = 0
        for img in range(image.get_width()/size[0]):
            img = pygame.Surface(size)
            if colorkey:
                img.set_colorkey((0,0,0))
            img.blit(image,(-x,-y))
            row.append(img)
            x += size[0]
        map.append(row)
        y += size[1]
    return map

class Animation(object):
    '''
    A sequence of images matching the FPS rate of the game to simulate
    an animation.
    '''

    def __init__(self, seq=[], loop=False):
        for image in seq:
            if type(image) == type('<string>'):
                seq[seq.index(image)] = pygame.image.load(image)

        self.index = 0
        self.loop = loop
        self.seq = seq
        self.surf = seq[0]

    def tick(self):
        if self.index == (len(self.seq)-1):
            if self.loop:
                self.index = 0
                self.surf = self.seq[0]
        else:
            self.index += 1
            self.surf = self.seq[self.index]

if __name__=='__main__':
    import glob,engine,sprite
    seq = glob.glob('exploBig/*.bmp')
    seq = [[pygame.image.load(img) for img in seq[:7]],
           [pygame.image.load(img) for img in seq[8:]]]
    saveGrid(seq,'temp.bmp')
    seq = loadGrid('temp.bmp',(40,40),(0,0,0))
    ani = seq [0]
    ani.extend(seq[1])
    ani = Animation(ani,loop=True)

    sprite.AnimatedSprite.anim = ani
    sprite = sprite.AnimatedSprite()

    s = engine.State()
    def tick(event):
        sprite.update()
        pygame.display.get_surface().fill((0,0,0))
        pygame.display.get_surface().blit(sprite.image,sprite.rect)
        pygame.display.flip()
    s.EVT_tick = tick
    e = engine.Engine(20)
    e.DEFAULT = s
    e.size = (300,200)
    e.run()

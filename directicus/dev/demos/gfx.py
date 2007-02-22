
if __name__=='__main__':
    import glob
    from directicus import engine,sprite
    from directicus.gfx import *
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

    s = engine.State
    def tick(self,event):
        sprite.update()
        pygame.display.get_surface().fill((0,0,0))
        pygame.display.get_surface().blit(sprite.image,sprite.rect)
        pygame.display.flip()
    s.EVT_tick = tick
    e = engine.Engine(20)
    e.DEFAULT = s
    e.size = (300,200)
    e.run()

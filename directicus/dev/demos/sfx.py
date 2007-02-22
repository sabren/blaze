
if __name__=='__main__':
    import glob
    from directicus import engine,gfx,sprite
    from directicus.sfx import *

    sfx = Audio()
    music = Music()

    def sound(e):
        sfx.play('explode.wav')

    def fade(self):
        self.start()
        sfx.stop(1000)

    sprite.AnimatedSprite.start = sound
    sprite.AnimatedSprite.onEnd = fade
    sprite.AnimatedSprite.anim = gfx.Animation(glob.glob('exploBig/*.bmp'),True)
    noisySprite = sprite.AnimatedSprite()

    def start(self):
        engine.State.start(self)
        noisySprite.start()
        sfx.volume = 0.3
        sfx.EVT_tick(None)
        music.volume = 1.0
        music.EVT_tick(None)
        music.play('water.wav')

    def tick(self,event):
        pygame.display.get_surface().fill((0,0,0))
        noisySprite.update()
        pygame.display.get_surface().blit(noisySprite.image,noisySprite.rect)
        pygame.display.flip()

    engine.Menu.EVT_tick = tick
    engine.Menu.start = start
    e = engine.Engine()
    e.size = (300,200)
    e.run()

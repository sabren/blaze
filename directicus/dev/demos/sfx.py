import directicus
from directicus.sfx import *
directicus.event.debugging = False

if __name__=='__main__':
    sfx = Audio()
    music = Music()

    class NoisySprite(directicus.sprite.AnimatedSprite):
        grid = directicus.gfx.GridSheet(filename='media/explode.png',size=(40,40))
        m = grid.getMatrix()
        seq = m[0]+m[1]
        anim = directicus.gfx.Animation(seq,True)

        def start(self):
            sfx.play('media/explode.wav')
    
        def onEnd(self):
            self.start()
            sfx.stop(1000)

    noisySprite = NoisySprite()
    noisySprite.rect.center = (150,100)
    
    class SoundDemo(directicus.engine.State):
        def start(self):
            directicus.engine.State.start(self)
            pygame.display.set_caption('Directicus Audio Demo')
            noisySprite.start()
            sfx.volume = 0.3
            sfx.onTick(None)
            music.volume = 1.0
            music.onTick(None)
            music.play('media/water.wav')
    
        def onTick(self,event):
            noisySprite.update()
            disp = pygame.display.get_surface()
            disp.fill((0,0,0))
            disp.blit(noisySprite.image,noisySprite.rect)
            pygame.display.flip()

    e = directicus.engine.Engine(20)
    e.DEFAULT = SoundDemo
    e.size = (300,200)
    e.run()
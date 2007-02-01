
import pygame, eventnet.driver, os

if not pygame.mixer.get_init():
    pygame.mixer.init()

class Audio(eventnet.driver.Handler):
    '''
    Audio engine with sound falloff.
    '''

    volume = 0.0
    sounds = []
    falloff = 0.0 #per-pixel volume falloff

    def __init__(self):
        eventnet.driver.Handler.__init__(self)
        self.capture()

    def EVT_tick(self,event):
        for sound in self.sounds:
            if sound.get_volume() != self.volume:
                sound.set_volume(self.volume)

    def _offset(self,pos=(0,0)):
        w,h = pygame.display.get_surface().get_size()
        x,y = pos

        xOffset = 0
        yOffset = 0

        if x < 0:
            xOffset = -x
        elif x > w:
            xOffset = x - w
        if y < 0:
            yOffset = -y
        elif y > h:
            yOffset = y - h

        return (yOffset + xOffset) * self.falloff

    def play(self,filename,loops=0,pos=(0,0)):
        '''
        Loads and plays a sound. loops is the number of times to play
        the sound over with -1 meaning indefinitely. pos is the position
        relative to the topleft of the screen.
        '''

        sound = pygame.mixer.Sound(filename)
        sound.set_volume(self.volume)
        sound.play(loops)
        self.sounds.append(sound)

        if pygame.display.get_surface():
            sound.set_volume(sound.get_volume() - self._offset(pos))

    def pause(self):
        '''
        Stop play but save position.
        '''

        pygame.mixer.pause()

    def resume(self):
        '''
        Resume from a paused state.
        '''

        pygame.mixer.unpause()

    def stop(self,time=0):
        '''
        Stops all sounds playing, if time is given fadeout over a certain number
        of milliseconds.
        '''

        pygame.mixer.fadeout(time)

class Music(Audio):
    '''
    A music controller.
    '''

    def __init__(self):
        Audio.__init__(self)

    def EVT_tick(self,event):
        if pygame.mixer.music.get_volume() != self.volume:
            pygame.mixer.music.set_volume(self.volume)

    def play(self,filename,loops=0):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play(loops)

    def pause(self):
        pygame.mixer.music.pause()

    def resume(self):
        pygame.mixer.music.unpause()

    def stop(self,time=0):
        pygame.mixer.music.fadeout(time)

if __name__=='__main__':
    import engine,gfx,sprite,glob

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

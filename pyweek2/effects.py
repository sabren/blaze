import pygame, jukebox, glob, os, random, math, eventnet.driver

class Animation(pygame.sprite.Sprite):
    def __init__(self, images, pos, groups=[]):
        pygame.sprite.Sprite.__init__(self, groups)
        self.images = images
        self.pos = pos
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self):
        self.images.remove(self.images[0])
        try:
            self.image = self.images[0]
        except:
            self.kill()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

class smoke(pygame.sprite.Sprite):
    def __init__(self, pos, course=(0,0), groups=[]):
        pygame.sprite.Sprite.__init__(self, groups)
        self.course = course
        self.image = pygame.Surface((50,50))
        self.image.fill((60,0,60))
        self.image.set_colorkey((60,0,60))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.alpha = 255
        self.radius = 3
        pygame.draw.circle(self.image, (100,100,100), (self.rect.width/2,
                                                       self.rect.height/2),
                           self.radius)

    def update(self):
        if self.alpha < 0:
            self.kill()
        else:
            self.alpha -= 15
            self.radius += 1
            pygame.draw.circle(self.image, (100,100,100), (self.rect.width/2,
                                                           self.rect.height/2),
                               self.radius)
            self.image.set_alpha(self.alpha)
            self.rect = self.rect.move(self.course)

class Effects:
    '''
    A class to handle smoke, explosions, and sounds.
    '''

    def __init__(self, screen, jkbx, background, smoke_pos=(-50, -50)):
        self.screen = screen
        self.jkbx = jkbx
        self.background = background
        self.water_sounds = glob.glob(os.path.join('data', 'sound',
                                                   'wave*'))+[os.path.join(
            'data', 'sound', 'water.wav')]
        self.water_sounds = [os.path.splitext(os.path.split(snd)[-1])[0]
                        for snd in self.water_sounds]
        random.shuffle(self.water_sounds, random.random)
        self.water_sound = self.water_sounds[0]
        self.explosion_sounds = glob.glob(
            os.path.join('data', 'sound', 'expl*'))+glob.glob(
                os.path.join('data', 'sound', 'mortar_explode*'))
        self.explosion_sounds = [os.path.splitext(os.path.split(snd)[-1])[0]
                                 for snd in self.explosion_sounds]
        self.shot = 'howitzer'
        self.splash_sounds = glob.glob(os.path.join('data', 'sound',
                                                    'water_splash*'))
        self.splash_sounds = [os.path.splitext(os.path.split(snd)[-1])[0]
                         for snd in self.splash_sounds]
        self.random_sounds = glob.glob(
            os.path.join('data', 'sound', 'metal_*'))+glob.glob(
                os.path.join('data', 'sound', 'Shaker*'))
        self.random_sounds = [os.path.splitext(os.path.split(snd)[-1])[0]
                              for snd in self.random_sounds]
        self.engine = 'engine'
        self.all_sounds = [
            self.shot, self.engine]+self.random_sounds+self.explosion_sounds+self.water_sounds+self.splash_sounds
        for sound in self.all_sounds:
            self.jkbx.load_sound(sound)
            self.jkbx.set_sound_volume(0.3, sound)
        self.jkbx.set_sound_volume(0.7, self.engine)
        self.jkbx.play_sound(self.engine, -1)
        self.explosion_seq = glob.glob(os.path.join('data', 'effects', 'exploBig',
                                                    '*.bmp'))
        self.explosion_seq.sort()
        self.explosion_seq = [
            pygame.image.load(img) for img in self.explosion_seq]
        for img in self.explosion_seq:
            img.set_colorkey((0,0,0))
        self.cannon_ball = pygame.image.load(os.path.join(
            'data', 'effects', 'shell.bmp'))
        self.smoke_pos = smoke_pos
        self.sprites = pygame.sprite.Group()

        self.shots = pygame.sprite.Group()

    def tick(self):
        if not self.jkbx.is_sound_playing(self.water_sound):
            random.shuffle(self.water_sounds, random.random)
            self.water_sound = self.water_sounds[0]
            self.jkbx.set_sound_volume(0.05, self.water_sound)
            self.jkbx.play_sound(self.water_sound)

        if not self.jkbx.is_sound_playing(self.random_sounds[0]):
            if random.randint(0, 4) == 0:
                random.shuffle(self.random_sounds, random.random)
                self.jkbx.set_sound_volume(0.05, self.random_sounds[0])
                self.jkbx.play_sound(self.random_sounds[0])

        for shot in self.shots.sprites():
            if shot.rect.center[0] > shot.end_pos[0]:
                x_diff = shot.rect.center[0] - shot.end_pos[0]
            else:
                x_diff = shot.end_pos[0] - shot.rect.center[0]
            if shot.rect.center[1] > shot.end_pos[1]:
                y_diff = shot.rect.center[1] - shot.end_pos[1]
            else:
                y_diff = shot.end_pos[1] - shot.rect.center[1]
            distance = x_diff + y_diff
            if distance < 40:
                shot.kill()
                self.explosion(shot.end_pos)
            else:
                shot.rect.center = (shot.rect.center[0] + (shot.course[0]/7),
                                    shot.rect.center[1] + (shot.course[1]/7))

        self.sprites.add(smoke(self.smoke_pos, (
            random.randint(-1, 1), random.randint(-1, 1))))

    def explosion(self, pos):
        self.jkbx.play_sound(self.explosion_sounds[random.randint(
            0,len(self.explosion_sounds)-1)])
        self.sprites.add(Animation([img for img in self.explosion_seq], pos))
        eventnet.driver.post('Explosion', pos=pos)

    def shoot(self, start_pos, end_pos):
        if start_pos != end_pos:
            y = end_pos[0] - start_pos[0]
            x = end_pos[1] - start_pos[1]
            if x == 0:
                x = 1
            if y == 0:
                y = 1
            angle = math.degrees(math.atan(float(y)/float(x)))
            if x < 0:
                angle += 179
            if angle < 0:
                angle += 360
            angle += 180

            shot = pygame.sprite.Sprite([self.shots, self.sprites])
            shot.image = self.cannon_ball
            shot.rect = shot.image.get_rect()
            shot.rect.center = start_pos
            self.jkbx.play_sound('howitzer')
            shot.course = (math.degrees(-math.sin(math.radians(angle))),
                           math.degrees(-math.cos(math.radians(angle))))
            shot.end_pos = end_pos

if __name__=='__main__':
    jkbx = jukebox.Jukebox()
    screen = pygame.display.set_mode((800,600))
    screen.fill((255,255,255))
    background = pygame.Surface((800,600))
    background.fill((255,255,255))
    fx = Effects(screen, jkbx, background, (50,0))
    fx.shoot((700,100), (700, 500))
    while 1:
        pygame.display.flip()
        fx.smoke_pos = (50, fx.smoke_pos[1]+5)
        fx.sprites.update()
        fx.sprites.clear(screen, background)
        fx.sprites.draw(screen)

        fx.tick()
        pygame.time.wait(75)

    

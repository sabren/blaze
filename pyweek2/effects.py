import pygame, jukebox, glob, os, random, math

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
        self.color = (0,0,0)
        self.radius = 10
        pygame.draw.circle(self.image, self.color, (self.rect.width/2,
                                                    self.rect.height/2),
                           self.radius)

    def update(self):
        if self.color[0] > 254:
            self.kill()
        else:
            self.color = (self.color[0]+15,
                          self.color[1]+15,
                          self.color[2]+15)
            self.radius += 1
            pygame.draw.circle(self.image, self.color, (self.rect.width/2,
                                                        self.rect.height/2),
                               self.radius)
            self.rect = self.rect.move(self.course)

class Effects:
    '''
    A class to handle smoke, explosions, and sounds.
    '''

    def __init__(self, jkbx, background, smoke_pos=(-50, -50)):
        self.jkbx = jkbx
        self.background = background
        self.water_sounds = glob.glob(os.path.join('data', 'sound',
                                                   'wave*'))+[os.path.join(
            'data', 'sound', 'water.wav')]
        self.water_sounds = [os.path.splitext(os.path.split(snd)[-1])[0]
                        for snd in self.water_sounds]
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
        for shot in self.shots.sprites():
            x_diff = shot.rect.center[0] - shot.end_pos[0]
            y_diff = shot.rect.center[1] - shot.end_pos[1]
            distance = x_diff + y_diff
            if distance < 5 and distance > -5:
                shot.kill()
                self.explosion(shot.end_pos)
            else:
                shot.rect.center = (shot.rect.center[0] + (shot.course[0]*20),
                                    shot.rect.center[1] + (shot.course[1]*20))

        self.sprites.update()
        self.sprites.clear(pygame.display.get_surface(), self.background)
        self.sprites.draw(pygame.display.get_surface())

        self.sprites.add(smoke(self.smoke_pos, (
            random.randint(-1, 1), random.randint(-1, 1))))

    def explosion(self, pos):
        self.jkbx.play_sound(self.explosion_sounds[random.randint(
            0,len(self.explosion_sounds)-1)])
        self.sprites.add(Animation(self.explosion_seq, pos))

    def shoot(self, start_pos, end_pos):
        if start_pos != end_pos:
            if start_pos[0] > end_pos[0]:
                x_diff = start_pos[0] - end_pos[0]
            else:
                x_diff = end_pos[0] - start_pos[0]
            if start_pos[1] > end_pos[1]:
                y_diff = start_pos[1] - end_pos[1]
            else:
                y_diff = end_pos[1] - start_pos[1]

            if y_diff == 0:
                y_diff = 1
            if x_diff == 0:
                x_diff = 1
            distance = y_diff + x_diff

            shot_seq = []
            angle = math.degrees(math.atan(float(x_diff)/float(y_diff)))
            shot = pygame.sprite.Sprite([self.shots, self.sprites])
            shot.image = self.cannon_ball
            shot.rect = shot.image.get_rect()
            shot.rect.center = start_pos
            self.jkbx.play_sound('howitzer')
            shot.course = (math.sin(math.radians(angle)),
                           math.cos(math.radians(angle)))
            shot.end_pos = end_pos

if __name__=='__main__':
    jkbx = jukebox.Jukebox()
    screen = pygame.display.set_mode((800,600))
    screen.fill((255,255,255))
    background = pygame.Surface((800,600))
    background.fill((255,255,255))
    fx = Effects(jkbx, background, (50,0))
    #fx.explosion((400,300))
    fx.shoot((700,100), (700, 500))
    while 1:
        pygame.display.flip()
        fx.smoke_pos = (50, fx.smoke_pos[1]+5)
        fx.tick()
        pygame.time.wait(75)

    

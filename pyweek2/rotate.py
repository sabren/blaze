import pygame, sys, math
pygame.init()
screen = pygame.display.set_mode((640,480))
img = pygame.Surface((100,100))
pygame.draw.line(img, (100,100,100),
                 (img.get_width()/2, img.get_height()/2),
                 (img.get_width()/2, (img.get_height()/2)-30), 3)
pygame.draw.circle(img, (127,127,127),
                   (img.get_width()/2, img.get_height()/2), 10)
angle = 0
i = img
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            a = event.dict['pos'][0] - screen.get_width()/2
            b = event.dict['pos'][1] - screen.get_height()/2
            if b == 0: b = 1
            if a == 0: a = 1
            angle = math.atan(float(a)/float(b)) * 57.295779513082323
            if b < 0: angle += 179
            if angle < 0: angle += 360
            angle += 180
            img = pygame.transform.rotate(i, angle)
        elif event.type == pygame.MOUSEBUTTONDOWN: pass
    screen.fill((255,255,255))
    screen.blit(img,
                (screen.get_width()/2-img.get_width()/2,
                 screen.get_height()/2-img.get_height()/2))
    pygame.display.flip()

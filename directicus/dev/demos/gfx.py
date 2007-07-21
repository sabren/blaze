import directicus,pygame
directicus.event.debugging = False

if __name__=='__main__':
    sheet = directicus.gfx.GridSheet(filename='media/explode.png',size=(40,40))
    m = sheet.getMatrix()
    seq = m[0]+m[1]
    anim = directicus.gfx.Animation(seq,True)
    
    class MyState(directicus.engine.State):
        def start(self):
            directicus.engine.State.start(self)
            pygame.display.set_caption('Directicus GridSheet and Animation Demo')
            
        def onTick(self,event):
            directicus.engine.State.onTick(self,event)
            disp = pygame.display.get_surface()
            disp.fill((0,0,0))
            disp.blit(anim.surf,(130,80))
            anim.tick()
            pygame.display.flip()
            
    e = directicus.engine.Engine(20)
    e.size = (300,200)
    e.DEFAULT = MyState
    e.run()
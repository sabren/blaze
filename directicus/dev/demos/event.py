from directicus.event import *
import directicus,sys,pygame

if __name__=='__main__':
    class MyListener(Listener):
        pass
    
    listener1 = MyListener()
    
    @eventListener(listener1)
    def onKeyDown(self,event):
        print '"%s" pressed!' % event.unicode
        
    class MyOtherListener(Listener):
        def onMouseButtonDown(self,event):
            print 'Mouse clicked!'
            
    listener2 = MyOtherListener()
    del listener2
        
    @eventListener
    def onQuit(event):
        print 'Bye, bye!'
        sys.exit()
        
    class EventDemo(directicus.engine.State):
        def start(self):
            directicus.engine.State.start(self)
            pygame.display.set_caption('Directicus Event Demo')

    e = directicus.engine.Engine()
    e.DEFAULT = EventDemo
    e.size = (300,200)
    e.run()
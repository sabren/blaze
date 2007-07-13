# Change this to turn off "event not handled" messages
debugging = True

prefix = 'on'

class Event(object):
    def __init__(self,type,**kwargs):
        object.__init__(self)
        self.dispatcher = dispatcher
        self.kwargs = kwargs
        self.__dict__.update(kwargs)
        self.type = type
        
    def __repr__(self):
        return '<Event %s %s>' % (str(self.type),
                                  ' '.join(['%s=%s' % arg for arg in self.kwargs.items()]))

class Dispatcher(object):
    handlers = {}

    def connect(self,type,handler):
        if not self.handlers.has_key(type):
            self.handlers[type] = list()
        self.handlers[type].append(handler)

    def disconnect(self,handler):
        for handlers in self.handlers.values():
            if handler in handlers:
                handlers.remove(handler)
                return
            
    def dispatch(self,eventType,**kwargs):
        event = Event(eventType,**kwargs)
        if eventType in self.handlers.keys():
            for handler in self.handlers[eventType]:
                if handler:
                    handler(event)
        elif debugging:
            print 'Unhandled event %s' % repr(event)

dispatcher = Dispatcher()

class Handler(object):
    def __init__(self,func,parent=None):
        object.__init__(self)
        self.parent = parent
        self.func = func
        self.dispatcher = dispatcher
        type = func.func_name[len(prefix):]
        self.type = type
        dispatcher.connect(type,self)
        
    def __call__(self,event):
        if self.parent:
            return self.func(event,self.parent)
        else:
            return self.func(event)

class HandlerFactory(object):
    
    def __init__(self,parent):
        object.__init__(self)
        self.parent = parent
        
    def __call__(self,func):
        return Handler(func,self.parent)
            
def eventListener(arg):
    if hasattr(arg,'func_name'):
        return Handler(arg)
    else:
        return HandlerFactory(arg)
    
dispatch = dispatcher.dispatch
    
def handlePygame():
    import pygame
    from pygame.event import event_name
    pygame.event.pump()
    for event in pygame.event.get():
        dispatch(event_name(event.type),**event.dict)
            
class Listener(object):
    def __init__(self):
        object.__init__(self)
        self.dispatcher = dispatcher
        self.register()
        
    def register(self):
        self.unRegister()
        for name in dir(self):
            attr = getattr(self,name)
            if name.startswith(prefix):
                Handler(attr)
                
    def unRegister(self):
        for name in dir(self):
            attr = getattr(self,name)
            if not isinstance(attr,Handler):
                continue
            self.dispatcher.disconnect(attr)
            
def test():
    debugging = True
    class myObject():pass
    myObject = myObject()
    
    @eventListener(myObject)
    def onKeyDown(self,event):
        print 'keydown!'
        
    class MyObject2(Listener):
        def onMouseButtonDown(self,event):
            print 'mousedown!'
            
    MyObject2 = MyObject2()
    del MyObject2
        
    @eventListener
    def onQuit(event):
        import sys
        sys.exit()
        
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((300,200))
    while True:
        handlePygame()
        
if __name__=='__main__':
    test()
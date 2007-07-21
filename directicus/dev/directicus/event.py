# Directicus
# Copyright (C) 2006-2007 Team Trailblazer

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

# Change this to turn off "event not handled" messages
debugging = True

prefix = 'on'

__all__ = ['Listener','dispatch','handlePygame','eventListener','debugging','prefix']

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
        self.dispatcher.connect(type,self)
        if parent:
            parent.attach(self)
        
    def __call__(self,event):
        if self.parent:
            return self.func(self.parent,event)
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
        
    def attach(self,handler):
        setattr(self,prefix+handler.type,handler)
        
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
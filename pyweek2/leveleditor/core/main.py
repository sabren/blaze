import pygame, eventnet.driver, sys, states
from view import LEView
from leveleditor.data.config import get_config
from leveleditor.data.objects import get_objects


class LevelEditor:
    def __init__(self):
        self.config = get_config()
        self.objects = get_objects()
        self.locations = {}
    def locate(self,what,where):
        if what not in self.objects: raise Exception("Invalid object")
        self.locations.setdefault(what,[]).append(where)

def main():
    le = LevelEditor()
    v = LEView(le)
    while not v.done: #mainloop
        #post pygame events to eventnet
        for event in pygame.event.get():
            eventnet.driver.post(pygame.event.event_name(event.type),
                                 **event.dict)
        v.tick()
    pygame.quit()
        
if __name__=='__main__':
    main()

#le = LevelEditor()
#print le.config
#print le.objects
#le.locate(le.objects[0],(45,34))
#le.locate(le.objects[0],(145,134))
#le.locate(le.objects[1],(545,134))
#print le.locations
#import pickle
#print pickle.loads(pickle.dumps(le.locations))
#print le.locations

"""
espionage: how to use eventnet

http://lgt.berlios.de/#eventnet <-- read that
"""
import unittest
import eventnet.driver


"""
okay, so eventnet is an event dispatch system and
eventnet.driver is pretty much a singleton
and everything just plugs into that. we don't
have to do anything special to set it up, just
create some listeners and start sending events.
"""

AN_EVENT="THE_BIG_EVENT"

class HowNotToUseEventNet(unittest.TestCase):

    def setUp(self):
        self.gotIt = False

    # I wanted to do it this way but it didn't work:
    @eventnet.driver.handle(AN_EVENT)
    def onEvent(self):
        self.gotIt = True
    
    def test(self):        
        assert not self.gotIt
        eventnet.driver.post(AN_EVENT)
        assert not self.gotIt # :/ too bad, too.


# you can use decorators for plain functions though:

GLOBAL = {}

@eventnet.driver.handle(AN_EVENT)
def onEvent(event):
    GLOBAL["gotIt"]=True


class HowToUseDecoratorsForHandlers(unittest.TestCase):
    def test(self):
        GLOBAL["gotIt"]=False
        eventnet.driver.post(AN_EVENT)
        assert GLOBAL["gotIt"]



# here is the right way for doing classes:

class EventHandler(eventnet.driver.Handler):

    def __init__(self):
        super(EventHandler, self).__init__()
        self.gotIt = False
        self.count = 0

    def EVT_THE_BIG_EVENT(self, event):
        self.gotIt = True
        self.count += 1


class HowToUseEventHandlerClasses(unittest.TestCase):
    def test(self):
        h = EventHandler()
        h.capture()
        assert not h.gotIt
        eventnet.driver.post(AN_EVENT)
        assert h.gotIt



class MultipleHandlersTest(unittest.TestCase):

    def test(self):
        
        a = EventHandler()
        b = EventHandler()
        c = EventHandler()
        
        a.capture()
        # b will not capture
        c.capture()
        
        eventnet.driver.post(AN_EVENT)
        assert a.gotIt
        assert not b.gotIt
        assert a.gotIt

        a.release()
        eventnet.driver.post(AN_EVENT)
        assert a.count == 1
        assert b.count == 0
        assert c.count == 2
    


if __name__=="__main__":
    unittest.main()

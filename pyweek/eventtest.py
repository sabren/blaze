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

"""
About Events:

[20:25] <sabren> think of it like this:

[20:25] <sabren> there's a field full of objects

[20:25] <sabren> like a soccer field

[20:26] <sabren> and the objects are all out there doing there thing

[20:26] <sabren> their

[20:26] <eykd> mcferrill: I know the syntax for handling events :)

[20:26] <sabren> and the event handler is a guy with a megaphone

[20:26] <sabren> and all of a sudden he yells "THE BLOOD SUGAR HAS CHANGED!!!"

[20:26] <sabren> now

[20:26] <sabren> most of the objects don't care about that

[20:26] <sabren> so they don't do anything

[20:27] <sabren> but one guy over in the corner...

[20:27] <sabren> his job is to update the blood sugar display

[20:27] <sabren> so he's registered to handle that event

[20:27] <sabren> and he does the right thing

[20:27] <sabren> so each object is its own little event handler

[20:27] <sabren> does that make sense?

[20:28] <sabren> the events keep us from having to constantly be checking for everyting all at once

[20:28] <eykd> Oh, so *any* object that has a method EVT_EVENT will trigger it when EVENT gets fired?

[20:28] <sabren> i hope so

[20:28] <sabren> we didn't test that.

[20:28] <sabren> let's try it
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

        ## now tell one to stop listening:
        a.release()
        eventnet.driver.post(AN_EVENT)
        assert a.count == 1
        assert b.count == 0
        assert c.count == 2




# now we want to make sure you can post something
# without having listeners...

class AnotherHandler(eventnet.driver.Handler):

    def __init__(self):
        super(EventHandler, self).__init__()
        self.gotAnotherEvent = False

    def EVT_ANOTHER_EVENT(self, event):
        self.gotAnotherEvent = True


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

        ## now tell one to stop listening:
        a.release()
        eventnet.driver.post(AN_EVENT)
        assert a.count == 1
        assert b.count == 0
        assert c.count == 2



    


if __name__=="__main__":
    unittest.main()

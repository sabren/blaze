import weakref

class Event(object):
    def __init__(self, *args, **kw):
        self.__dict__.update(kw)
        self.args = kw
        self.type = args[0]
    def __repr__(self):
        return '<Event %s %s>' % (str(self.type), " ".join([("%s=%s" % i) for i in self.args.items()]))

class Observer(object):
    __slots__ = ['events']
    def __init__(self):
        self.events = {}

    def register(self, who, eventtypes):
        """
        Register a Listener for a list of event types.
        The listener will receive any events it is registered for.
        """
        try:
            callback = who.dispatch
        except AttributeError:
            callback = who

        for eventtype in eventtypes:
            try:
                self.events[eventtype].append(callback)
            except KeyError:
                self.events[eventtype] = []
                self.events[eventtype].append(callback)

    def unregister(self, who):
        """Remove an event Listener. The listener will no longer receive events."""
        remove = []
        for event in self.events:
            if who in self.events[event]:
                self.events[event].remove(who)

    def post(self, eventType, **kw):
        """Post an event, which is dispatched to registered listeners."""
        e = []
        if eventType in self.events: e = self.events[eventType]
        #print "POST:", const.lookup(eventType), kw, e
        if eventType in self.events:
            event = Event(eventType, **kw)
            for func in self.events[event.type]:
                if func: func(event)
            return self.events[event.type]
        else:
            return []

class Handler(object):
    def __init__(self, observer, events=[]):
        """Creates a handler object which listens and posts to an Observer for events."""
        self.observer = observer
        self.observer.register(self, events)
        self.post = self.observer.post

    def dispatch(self, event):
        """Called when the self.observer has an event for self to process."""
        pass

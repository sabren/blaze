import baseevent

observer = baseevent.Observer()
post = observer.post

handler_prefix = "EVT_"

class handle(object):
    "A decorator which will register a function to handle an event."
    def __init__(self, *args):
        self.events = args
    def __call__(self, func):
        self.func = func
        observer.register(func, self.events)
        return self

    def kill(self):
        observer.unregister(self.func)


class Handler(object):
    def __init__(self, prefix=handler_prefix):
        self.handler_prefix = prefix
    def capture(self):
        for meth in dir(self):
            if self.handler_prefix in meth[:len(self.handler_prefix)]:
                name = meth[len(self.handler_prefix):]
                observer.register(getattr(self, meth), [name])

    def release(self):
        for meth in dir(self):
            if self.handler_prefix in meth[:len(self.handler_prefix)]:
                observer.unregister(getattr(self, meth))




if __name__ == "__main__":
    class Test(Handler):
        def __init__(self):
            Handler.__init__(self)

        def EVT_A(self, event):
            print event

    t = Test()
    t.capture()
    post('A',b=1)
    t.release()

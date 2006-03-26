import pygame, eventnet.driver, states

class View(eventnet.driver.Subscriber):
    def __init__(self):
        pygame.init()
        self.capture()
        self.done = False
        self.screen = pygame.display.set_mode((800, 600)) #windowed for now
        self.load_default_state()
    def tick(self):
        if not self.state.done:
            self.state.tick()
        elif self.state.next <> None:
            self.state = self.state.next
        else: self.load_default_state()
    def load_default_state(self):
        try: self.state.quit()
        except: pass
        self.state = states.Menu(self.screen)
        self.state.start()

    def EVT_Quit(self):
        self.release()
        self.done = True

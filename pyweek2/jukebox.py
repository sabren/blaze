import pygame,os

class Jukebox:

    """
    Class for handling music and sound, you load them up, and then play the 
    sounds by name, and the songs by name or randomly.
    This should be enough for a start.
    """

    frequency = 22050
    size = -16
    stereo = True
    buffer = 2048
    def __init__(self):
        try:
            pygame.mixer.pre_init(self.frequency,self.size,self.stereo,self.buffer)
            pygame.mixer.init()
        except Exception,e:
            print e
            raise
        self.soundlist = {}
        self.songlist = {}
        self.current_song = None
        self.current_sound = None
        self.datadir = '/home/vinko/pygame/pyweek2/data' #This should be grabbed from a config class or something
        self.channels = pygame.mixer.get_num_channels()
    
    def load_sound(self,file,ext=".wav"):
        """
        Loads a sound to the jukebox, the 'file' arg is actually the key to a dict that can be used then to reference it.
        It's supposed to be a mnemonic name (the actual file should have this name too, for instance boom1.wav, is
        passed as boom1
        """
        filename = os.path.join(self.datadir,file+ext)
        if os.path.exists(filename):
            self.soundlist[file] = pygame.mixer.Sound(filename)
        else:
            raise Exception("File not found %s" % filename)
    
    def load_song(self,file,ext=".wav"):
        filename = os.path.join(self.datadir,file+ext)
        if os.path.exists(filename):
            self.songlist[file] = filename
            self.current_song = file

    def play_song(self,name=None,loops=0,start=0.0):
        """
        The mnemonic of the song, loops is how many times will it play, and start
        is the starting position. All args are optional, if no name specified, will play the last
        song loaded
        """
        if not name is None:
            try:
                pygame.mixer.music.load(self.songlist[name])
                pygame.mixer.music.play(loops,start)
                self.current_song = name
            except KeyError,e:
                pass
        else:
            pygame.mixer.music.load(self.songlist[self.current_song])
            pygame.mixer.music.play(loops,start)
        
    def play_sound(self,name,loops=0,maxtime=0):
        """
        Here the name is not optional, as I think sounds shouldn't be played by load ordering or randomly
        """
        self.soundlist[name].play(loops,maxtime)
        self.current_sound = name

    def stop_sound(self,name=None):
        """
        Stops sound by name or by current if name is omitted
        """
        if not name is None:
            self.soundlist[name].stop()
        else:
            self.soundlist[self.current_sound].stop()

    def stop_song(self,fade=True,time=1.0):
        """
        If fade, the song will fadeout instead of stopping abruptly, time is how many seconds the
        fade will last
        """
        if fade:
            pygame.mixer.music.fadeout(time)
        pygame.mixer.music.stop()
        
    def play_random_song(self,loops=0,start=0.0):
        import random
        self.current_song = self.songlist[random.choice(self.songlist)]
        self.play_song(self.current_song,loops,start)
    
    

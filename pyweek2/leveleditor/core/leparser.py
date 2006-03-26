import os
from object import GameObject

#Location of the config files, relative to the main game dir
DATADIR = "leveleditor/data/"

class LEParser:
    def __init__(self):
        pass
    def read_config(self):
        """
        Reads the main level editor config file, returning a dict of key/value pairs.
        The format expected is 'key = value\n'
        The file is to be called 'os.path.join(DATADIR,'main')'
        Current config options:
        sprites_path = Base location of the sprites (will be added to the objects' sprite config option)
        screen_size = Size of the screen to be created (widthxheight)
        sprite_size = Size of the sprites
        tile_size = Size of the tiles
        """
        global DATADIR
        config = {}
        mainconfig = open(os.path.join(DATADIR,"main"),"r").read()
        arr_data = mainconfig.split(os.linesep)
        for line in arr_data:
            line = line.split('=')
            if len(line) == 2:
                config[line[0].strip()] = line[1].strip()
        return config
    def read_objects(self):
        """
        Reads the all the objects files, returning a list of GameObjects.
        Each object file (located under DATADIR) has to have the following options defined (required for each GameObject)
        There cannot be an object file called 'main' for obvious reasons
        Current options are:
        name = Name of the object
        sprite = Name of the image that represents the object, will append config option sprites_path to it
        """
        global DATADIR
        objects = {}
        for file in os.listdir(DATADIR):
            if file !='main' and not os.path.isdir(file):
                content = open(os.path.join(DATADIR,file),"r").read()
                for line in content.split(os.linesep):
                    line = line.split('=')
                    if len(line) == 2:
                        objects.setdefault(line[0].strip(),[]).append(line[1].strip())
        object_list = []
        for name,sprite in zip(objects['name'],objects['sprite']):
            object_list.append(GameObject(name,sprite))
        return object_list

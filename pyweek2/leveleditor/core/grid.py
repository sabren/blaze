import pygame,os,pickle
class Grid:
    def __init__(self,width,height,tile_size,screen_size,screen):
        self.width, self.height, self.tile_size,self.screen_size,self.screen = width,height,tile_size,screen_size,screen
        if self.width < self.screen_size[0]:
            self.width_ratio = self.width / float(self.screen_size[0])
        else:
            self.width_ratio = float(self.screen_size[0]) / self.width
        self.display_tile_size = int(self.tile_size * self.width_ratio)
        self.rows =  self.height/self.display_tile_size
        self.columns = self.width/self.display_tile_size
        self.matrix = map(list,self.rows*[self.columns*[None]])
        self.init_grid()

    def init_grid(self):
        pos_hor = 140
        pos_ver = 0
        for i in xrange(self.rows+1):
            r = pygame.Rect(pos_hor,0,1,600)
            pos_hor += self.display_tile_size
            self.screen.fill((0,0,0),r) 
        pos_hor = 140
        final_width = self.rows*self.display_tile_size
        for i in xrange(self.columns+1):
            r = pygame.Rect(pos_hor,pos_ver,final_width,1)
            pos_ver += self.display_tile_size
            self.screen.fill((0,0,0),r) 
        pygame.display.flip()
    
    def add_object_in_pos(self,object,pos):
        if object is None: 
            print "You haven't selected a thing!"
            return
        x,y = self.get_matrix_indexes(pos)
        try:
            self.matrix[x][y] = object.name #Or a hash?
        except IndexError:
            print "You have clicked outside of the grid!"
        self.print_non_nones()
    def get_matrix_indexes(self,pos):
        cx = pos[0] - 140
        if cx <= 0: return self.rows,self.columns
        cy = pos[1]
        cx = cx/self.display_tile_size
        cy = cy/self.display_tile_size
        return cx,cy
    def print_non_nones(self):
        print "------------------------------------------------"
        for i in xrange(self.rows):
            for j in xrange(self.columns):
                if not self.matrix[i][j] is None:
                    print "MATRIX[%s][%s] is %s" % (i,j,self.matrix[i][j],)
        print "------------------------------------------------"
    def save_level(self):
        print "BEFORE SAVING:"
        self.print_non_nones()
        strmatrix = pickle.dumps(self.matrix)
        f = open("temporarylevel.pic","wb")
        f.write(strmatrix)
        f.close()
        self.load_level()
        print "AFTER SAVING AND RELOADING:"
        self.print_non_nones()
    def load_level(self):
        if os.path.exists("temporarylevel.pic"):
            self.matrix = pickle.loads(open("temporarylevel.pic","rb").read())
    def render(self):
        pass

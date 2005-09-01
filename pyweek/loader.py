"""
load rooms from svg description

usage: loader.roomFromFile(f)
"""

##################################################

"""

So. Our level is defined in an svg file created in inkscape.

From a physics standpoint, our world is composed of:

    - boxes
    - possibly arbitrary shapes if time
    - possibly spheres (or cylinders) if needed

All of these are defined as simple 2d primitives on a "physics" layer
in inkscape and simply mapped to their equivalent 3d shapes in
pyODE. (Arbitrary shapes will take some kind of extra work, hence
'possibly'


Since we know the world consists only of primitives, then that
simplifies our xml parser considerably: the parts will never
nest, so we just need to find the right tags.

"""

import ode
import unittest
import physics
import xml.sax

from ode_to_pixel import *


"""
So let's start with boxes because it's the only one we
know we need. The SVG equivalent of a box is a rect.

Inkscape adds a bunch of attributes for style,
etc, but we only care about a few:

  width, height, x, y, and transform

inkscape uses matrix transforms, which we will have to
map to a rotation in pyODE...
"""


############################################################
##
## GOAL: convert our svg level to a list of Rects
## 
############################################################


# our scene is just a chunk of svg code.
# we only care about the rect elements, and we're
# assuming that we're only dealing with a single
# layer - the that defines the blocks.

# here is how inkscape saves a rotated rectangle:

SCENE =\
    '''
  <g
     id="layer1"
     inkscape:label="Layer 1"
     inkscape:groupmode="layer"
     style="display:inline">
    <rect
       width="198.86618"
       height="21.259426"
       x="102.61992"
       y="58.551853"
       transform="matrix(0.854241,0.519878,-0.519878,0.854241,0.000000,0.000000)" />
       </g>
    '''


# and here's how we want the parsing to work:

class ParserTest(unittest.TestCase):
    """
    test that we can get a list
    of rectangles from the svg file,
    in this case we want the one rectangle
    defined in the string above.
    """

    def test(self):
        svgh = SvgHandler() 
        xml.sax.parseString(SCENE, svgh)

        assert type(svgh.result) is list
        assert len(svgh.result) == 1

        r = svgh.result[0]
        assert isinstance(r, Rect)

        self.assertEquals(float(u"102.61992"), r.x)
        self.assertEquals(float(u"198.86618"), r.width)
        self.assertEquals(float(u"21.259426"), r.height)

        # this one is a little tricky:
        # in svg and pyode, y++ is upward motion,
        # (in other words, (0,0) is lower left)
        #
        # but in pygame, y++ is downward motion
        # (so (0,0) is upper left)
        #
        # since pygame is the one we actually see,
        # it takes precedence, and so we flip the y:
        self.assertEquals(float(u"58.551853"), r.y)

        self.assertEquals([0.854241,0.519878,-0.519878,
                           0.854241,0.000000,0.000000],
                           r.transform)



# so... to make that work, we need to define an
# object to hold our rectangle data:

class Rect:
    """
    A simple data class for representing rectangles.
    """
    def __init__(self, x=0, y=0, width=0, height=0, transform=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.transform = transform

    # we will need this later:
    def getCenter(self):
        return ((self.width / 2.0 + self.x),
                (self.height / 2.0 + self.y))


# now we just loop through the tags in the SVG file
# and build up a list of Rect objects.
#
# we use a sax ContentHandler for this.
# you can use it with:
#
# svgh = SvgHandler() 
# xml.sax.parseString(xml_string, svgh)


class SvgHandler(xml.sax.ContentHandler):
    """
    parse the SVG file and build a list of rects
    """
    def __init__(self):
        self.result = []

    def startElement(self, name, attrs):
        if name =="rect":
            r = Rect()
            self.result.append(r)

            for attr, value in attrs.items():
                if attr in ["x","width","height"]:
                    setattr(r, attr, float(value))
                elif attr == "y":
                    r.y = float(value) #@TODO: HEIGHT
                elif attr == "transform":
                    r.transform = parseMatrix(value)



# the only tricky part of parsing the tags is the
# transformation attribute, which uses a matrix()
# definition. but it's not that hard to parse:

"""
here's how we break that matrix data down into a list:
"""
def parseMatrix(s):
    data = s
    data = data.lstrip("matrix(")
    data = data.rstrip(")")
    return map(float, data.split(","))



# that's it. the test passes.



############################################################
##
## GOAL: RoomLoader : convert list of Rects into a Room
## 
############################################################

"""
Rooms contain our 3D geometry, which is really
just 2D geometry with a uniform depth to make
pyODE happy.

Room already has an .addGeom(cx, cy, lx, ly)
but svg gives us: x, y, w, h, and transform.

Room.addGeom(...) actually makes the ode.GeomBoxes,
so we only have two jobs:

   - calculate the center of the rect (cx, cy)

   - apply the matrix transformation


Calculating the center is easy. We know the width
and height so we just divide by half and add that
to the upper left corner. The code is already
back up there in Rect.getCenter()

We didn't test it yet, though, so:
"""

class RectCenterTest(unittest.TestCase):
    def test(self):
        r = Rect(0, 10, width=100, height=9)
        self.assertEquals((50, 14.5), r.getCenter())


"""
That gives us cx and cy. Then lx and ly are
just ODE words for width and height, so calling
Room.addGeom(cx, cy, lx, ly) is trivial.

We also need to do this matrix transformation, though
and while the code for that is also simple, it has a
little bit more conceptual overhead.
"""


## Transformation Matrices #################################

# reference:
# http://www.w3.org/TR/SVG11/coords.html#TransformMatrixDefined

"""

ODE needs a 3x3 transformation matrix, like this:

    | a c e |
    | b d f |
    | 0 0 1 |

That's a 3D transformation matrix. How they work is way
over my head, but luckily ODE handles it all for us.
However, there is a small problem: SVG is all 2D, which
works out so that the bottom row is always 0 0 1 . Since
these values are constant, svg's matrix operator doesn't
include them. Instead, of nine values, we get six, like so:


  matrix( 0.854241,  # a =  cos(r)
          0.519878,  # b =  sin(r)
         -0.519878,  # c = -sin(r)
          0.854241,  # d =  cos(r)
          0.000000,  # e 
          0.000000)  # f

          # where r is the angle of rotation


So we need to fill in the missing (0 0 1) and
put them in the right order for pyODE.

"""

from room import Room

# Applying this matrix should do
# nothing, so it's the identity
# matrix. 
IDENTITY3D = [1.0, 0.0, 0.0,  # a b 0
              0.0, 1.0, 0.0,  # c d 0
              0.0, 0.0, 1.0]  # e f 1

IDENTITY2D = [1.0, 0.0,       # a b
              0.0, 1.0,       # c d
              0.0, 0.0]       # e f



# Note, I am not 100% sure that these orderings are
# correct: you could serialize a matrix by doing the
# columns then the rows, or by doing the rows and then
# the columns. I know I have the 2D stuff correct
# because it's explained clearly on thw w3.org page
# that I linked above.

# the question is which order pyODE takes. I was not
# able to find this in the documentation. However,
# if you look at testRotation below, it *seems* to
# show that the numbers are in the correct places
# given the pattern above.

# basically, this implementation is an educated guess.

class RoomFromRectsTest(unittest.TestCase):

    def testPlain(self):
        """
        if we don't pass in a transformation, we
        should just get back the identity matrix
        (it's of course the default for ode.Geom)
        """
        rm = roomFromRects([Rect(0, 0, width=100, height=10,)])
        self.assertEquals(IDENTITY3D, rm.blocks[0].getRotation())

    def testIdentity(self):
        """
        if we pass in a 2D version of the
        identity matrix then we should
        still get the 3D one back
        """
        rm = roomFromRects([Rect(0, 0, width=100, height=10,
                                 transform=IDENTITY2D)])
        self.assertEquals(IDENTITY3D, rm.blocks[0].getRotation())


    def testRotation(self):
        """
        if we pass in a real matrix, then it
        should give us the 3D matrix.
        """
        import math
        a =  math.cos(math.pi)
        b =  math.sin(math.pi)
        c = -math.sin(math.pi)
        d =  math.cos(math.pi)
        e =  0
        f =  0
        rm = roomFromRects([Rect(0, 0, width=100, height=10,
                                 transform=[a,b,c,d,e,f])])
        self.assertEquals(
            [a, b, 0,
             c, d, 0,
             e, f, 1],
            rm.blocks[0].getRotation())
        
        


def roomFromRects(rects):
    """
    here's where we actually do the work.
    """
    rm = Room()
    print rects
    for r in rects:
        block = rm.addGeom(pixel2world(*r.getCenter()), px2w(r.width), px2w(r.height))
        if r.transform:
            a, b, c, d, e, f = r.transform
            block.setRotation((a,b,0,c,d,0,e,f,1))
    return rm
            


# with that, the tests pass... so the evidence supports
# this implementation, but i don't feel like i've quite
# proved it beyond a shadow of a doubt.

# but, there's nothing more to do until someone finds a
# counterexample, so, I'll tentatively mark this complete.

# so... onto something easy. :)

############################################################
##
## GOAL: utility script to make it easy to load a room.
## 
############################################################

# helper routines:

def rectsFromFile(f):
    svg = SvgHandler()
    xml.sax.parse(f, svg)
    return svg.result

def roomFromFile(f):
    """
    most likely, this is the one you want to call.
    """
    return roomFromRects(rectsFromFile(f))


 
if __name__=="__main__":
    unittest.main()    
    

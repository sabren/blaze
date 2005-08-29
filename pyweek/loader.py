
"""

So, our level is defined in an svg file created in inkscape.
No pgu.
:()

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


"""
So let's start with boxes because it's the only one we
know we need. The SVG equivalent of a box is a rect.

Inkscape adds a bunch of attributes for style,
etc, but we only care about a few:

  width, height, x, y, and transform

inkscape uses matrix transforms, which we will have to
map to a rotation in pyODE...
"""

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


import xml.sax

class ParserTest(unittest.TestCase):
    """
    test that we can get a list
    of rectangles from the svg file.
    """

    def test(self):
        svgh = SvgHandler() 
        xml.sax.parseString(SCENE, svgh)

        assert type(svgh.result) is list

        r = svgh.result[0]
        assert isinstance(r, Rect)

        self.assertEquals(float(u"102.61992"), r.x)
        self.assertEquals(float(u"58.551853"), r.y)
        self.assertEquals(float(u"198.86618"), r.width)
        self.assertEquals(float(u"21.259426"), r.height)

        self.assertEquals([0.854241,0.519878,-0.519878,
                           0.854241,0.000000,0.000000],
                           r.transform)




class Rect:
    """
    A holder claass for our Rectangles
    """
    def __init__(self):
        self.x = None
        self.y = None
        self.width = None
        self.height = None
        self.transform = None


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

            for attr, value in attrs.items(): #getNames():
                if attr in ["x","y","width","height"]:
                    setattr(r, attr, float(value)) # attrs.getValue(x)))
                elif attr == "transform":
                    r.transform = parseMatrix(value) #attrs.getValue(x))
                  

"""
here's how we break that matrix data down into a list:
"""
def parseMatrix(s):
    data = s
    data = data.lstrip("matrix(")
    data = data.rstrip(")")
    return map(float, data.split(","))




class ExtrusionTest(unittest.TestCase):
    def test(self):
        r = Rect()
        r.x, r.y = (0, 0) # upper left corner
        r.width = 100
        r.height = 10     # so lower right is (100, 10)



        #box = extrude(Re
        
        #box.y = -r.y
        #box.x = r.x
        


# interactive:
# http://www.rfbarrow.btinternet.co.uk/htmasa2/Matrix2D1.htm


# why there are six elements when ode wants 3x3:
# http://www.w3.org/TR/SVG11/coords.html#TransformMatrixDefined


#matrix( 0.854241,  # a / cos(a)
#        0.519878,  # b / sin(a)
#        -0.519878, # c / -sin(a)
#        0.854241,  # d / cos(a)
#        0.000000,  # e 0
#        0.000000)  # f 0

# "rotation about the origin is equivlanet to:
# [cos(a) sin(a) -sin(a) cos(a) 0 0]"


# Mathematically, all transformations can be represented as 3x3
# transformation matrices of the following form:

# | a c e |
# | b d f |
# | 0 0 1 |


# so this maps cleanly to pyODE:
#
# http://ode.org/ode-latest-userguide.html#sec_10_6_2
# http://pyode.sourceforge.net/api/public/ode.GeomObject-class.html#setRotation
#
 
if __name__=="__main__":
    unittest.main()    
    

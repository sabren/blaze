"""
rotation routine

This is a simple routine to rotate a point around the origin.
The reasons we need this is because in svg, rotation happens
around the origin *after* the x,y are found.

say you have a rectangle like this:

Y    a _b
|    / /
|   /_/
|   c  d
|
+--------X

(Yes, due to ascii limitiations, that's just a
parallelogram, but pretend it's a rectangle with
all right angles)

If you rotate that rectangle around the origin, 
you will find four positions where the rectangle
is at right angles to the x and y axis. For example,
if you start rotating clockwise, pretty soon the
rectangle will be in the lower right quadrant,
point c will be in the upper left hand corner, and segment
c-a will be parallel to the X axis.

Continue rotating into the lower left quadrant, and soon
point d will be in the upper left hand corner,
and d-c will be the oone parallel to the X axis.

And so on.

The idea is that in the drawing above, any of those points
could have been the "upper left corner" prior to a rotation
around the origin.

Well, so what? Well, turns out svg describes all rotations
this way: as rotations around the orgin starting with some
point (x,y) being in the upper left hand corner. That's what
this means:

<rect x="..." y="..." transform="matrix(....)"/>

In SVG, the x and y correspond to the upper left hand corner
of the rectangle BEFORE it was rotated around the origin.
This means that there for any rectangle that has a transformation
matrix, there are four possible "original" x and y coordinates.

That means a rectangle can be in the middle of the screen
(centered around point (300,300), say) but still have negative x and y
coordinates, because the rotation matrix gets applied *after*
the rectangle is initially positioned.

All of this means that if we want to tell pyODE where the center
of the rectangle is, then we have to do the math ourselves.

So here's what we need to do:


1. LOCATE THE ORIGINAL CENTER

   That's easy, because rect (from loader.py) already has a .getCenter()

2. APPLY THE TRANSFORMATION TO THE OLD CENTER TO GET THE NEW CENTER

3. TELL PYODE WHERE THE NEW CENTER IS, AND PASS IT THE
   TRANSFORMATION SO IT CAN ROTATE THE WHOLE GEOMBOX.

   Even though we're putting the center in the right place, ode
   still needs the transformation matrix so it can rotate the
   GeomBox around its center.  It doesn't matter which point
   you use for the center of rotation: for a given amount of
   rotation, you always get the same orientation in your rectangle,
   no matter where the center of rotation is. the only thing that
   changes if you change the center of rotation is where the
   rectangle ends up. So: we put the center in the right place
   and then pass in the same transformation matrix for pyode to use.


So, the only part that's tricky is step 2: actually performing the
transformation. Only it's not really that tricky, because it's
just a matrix operation. We would probably use numeric for this
if it were in the main loop, but since it's just for the loader:
"""
import math
def rotate((x,y), (a,b,c,d,e,f)):
    # these are some characteristics of a well formed rotation:
    #assert e == f == 0, "can't handle other kinds of matrices"
    #assert a == d, "a should equal d, but %s!=%s" % (a,d)
    #assert b == -c, "b should equal -c, but %s!=%s" % (b, -c)
    newx = (x * a) - (y * c)    
    newy = (x * b) + (y * d)
    return (newx, newy)


"""
for example, if you're at 0,1 and rotate 90 degrees, you should be at 1,0
"""
import unittest
class RotateTest(unittest.TestCase):
    def test(self):
        self.assertEquals((1,0), rotate((0,1), (0,1,-1,0,0,0)))

if __name__=="__main__":
    unittest.main()
    


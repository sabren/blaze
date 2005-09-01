
# this makes an asterisk
import math

print "<svg>"
print "<g>"

# dump a transformation matrix. rotation is:
#
# | cos(a)  -sin(a)   0  | a c 0 
# | sin(a)   cos(a)   0  | b d 0
# | 0        0        1  |
#
def makeRotatedRect(theta):
        a = math.cos(theta)
        b = math.sin(theta)
        c = -math.sin(theta)
        d = math.cos(theta)
        print '<rect style="fill:#ccff00" width="100" height="25" x="0" y="0"'
        print 'transform="matrix(%s,%s,%s,%s,0,0)"/>' % (a,b,c,d)

# print one without a rotation
#print '<rect style="fill:#993366" width="100" height="10" x="50" y="50"/>'


# goal is to go around in a circle, using radians
# there are 2*pi radians in a circle, so:
theta = 0
while theta < 2*math.pi:
    makeRotatedRect(theta)
    theta += math.pi/4


print "</g>"
print "</svg>"

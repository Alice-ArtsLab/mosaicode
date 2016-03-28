import math

def Psub(p1,p0):
    return p1[0]-p0[0],p1[1]-p0[1]

def Psum(p1,p0):
    return p1[0]+p0[0],p1[1]+p0[1]

def CordModDec(Vector):
    ans = []
    for e in Vector:
        ans.append(e)
    
    for e in range(len(ans)):
        if ans[e] > 0:
            ans[e] -= 1
        else:
            ans[e] += 1
    
    return (ans[0],ans[1])

def ColorFromList(rgba):
    color = int(rgba[0])*0x1000000+int(rgba[1])*0x10000+int(rgba[2])*0x100+(int(rgba[3])*0x01)
    return color
    
def Dist(p1,p2):
    return math.sqrt( math.pow(p2[0]-p1[0],2) + math.pow(p2[1]-p1[1],2))

def MakeArc(radius, edges, q=1):
    t_oPoints = []
    sin = math.sin
    cos = math.cos
    pi2 = (math.pi/2)
    for i in xrange(edges + 1):
        n = (pi2 * i) / edges + pi2*q
        t_oPoints.append((cos(n) * radius, sin(n) * radius))
    return t_oPoints

def AlterArc(arc, offsetx=0, offsety=0):
    return [(x+offsetx, y+offsety) for x, y in arc]

def ColorFromList(rgba):
    color = int(rgba[0])*0x1000000+int(rgba[1])*0x10000+int(rgba[2])*0x100+(int(rgba[3])*0x01)
    return color

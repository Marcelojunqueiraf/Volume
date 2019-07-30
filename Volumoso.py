import pygame
import math

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((500,500))

class Angle: #Stores 2 angles
    def __init__(self,tup): #defined by a tuple
        if type(tup)==tuple:
            self.pair = tup
        if type(tup)==Angle:
            self = tup
    
    def __str__(self):
        return str(self.pair)

    @property
    def pair(self): #tuple form
        return (self.x,self.y)

    @pair.setter
    def pair(self,value):
        self.x, self.y = value #x y form

class Vector3:
    def __init__(self,tup): #defined by a tuple
        if type(tup)==Vector3:
            tup = tup.coords
        self.coords = tup

    def __str__(self):
        return str(self.coords)
    
    @property
    def coords(self): #tuple form
        return (self.x,self.y,self.z)  

    @coords.setter
    def coords(self,value): 
        self.x, self.y, self.z = value # x y z form

    def __add__(self,b): #adds vectors (x+x,y+y,z+z)
        a = self
        if type(b) == Vector3:
            return Vector3((a.x+b.x, a.y+b.y, a.z+b.z))
        if type(b) == tuple:
            return Vector3((a.x+b[0], a.y+b[1], a.z+b[2]))

    def __iadd__(self, b):
        return self + b

    def __sub__(self, b):
        a = self
        if type(b) == Vector3:
            return Vector3((a.x-b.x, a.y-b.y, a.z-b.z))
        if type(b) == tuple:
            return Vector3((a.x-b[0], a.y-b[1], a.z-b[2]))

    def __isub__(self, b):
        return self - b

    @property
    def magnitude(self): #get the vector's magnitude
        return (self.x**2 + self.y**2 + self.z**2)**(1/3)
    
    def translate(self, value): #Adds a vector to self's vector
        self.coords = (self.x+value.x, self.y+value.y, self.z+value.z)
    
    def rotateX(self, a):
        ang = math.atan2(self.y,self.z)
        #print("Ang:{} a:{}".format(ang,a))
        ang -= a
        m = math.hypot(self.y,self.z)
        self.y = math.sin(ang)*m
        self.z = math.cos(ang)*m

    def rotateY(self, a):
        ang = math.atan2(self.z, self.x)
        ang -= a
        m = math.hypot(self.z,self.x)
        self.z = math.sin(ang)*m
        self.x = math.cos(ang)*m 

    def rotateZ(self, a):
        ang = math.atan2(self.y,self.x)
        ang -= a
        m = math.hypot(self.y,self.x)
        self.y = math.sin(ang)*m
        self.x = math.cos(ang)*m



class GameObject:
    allGO = []
    def __init__(self, pos = (0, 0, 0), sc = (10, 10, 10)):
        self.position = Vector3(pos)
        self.scale = Vector3(sc)
        self.allGO.append(self)

    def drawAll(cam):
        for go in GameObject.allGO:
            go.draw(cam)

    def draw(self, cam): 
        pos = self.position
        sc = self.scale
        pos += (-sc.x/2,-sc.y/2, -sc.z/2)

        p = []
        for x in range(2):
            for y in range(2):
                for z in range(2):
                    p.append(pos+(x*sc.x,y*sc.y,z*sc.z))

        cam.drawLine(p[0],p[2])
        cam.drawLine(p[0],p[4]) 
        cam.drawLine(p[2],p[6])
        cam.drawLine(p[4],p[6])

        cam.drawLine(p[0],p[4]) 
        cam.drawLine(p[1],p[3])
        cam.drawLine(p[1],p[5]) 
        cam.drawLine(p[3],p[7])
        cam.drawLine(p[5],p[7])

        cam.drawLine(p[0],p[1])
        cam.drawLine(p[2],p[3]) 
        cam.drawLine(p[4],p[5])
        cam.drawLine(p[6],p[7])


class Camera:
    def __init__(self, pos=(0,0,0), rot=(0,0), openning = 1):
        self.position = Vector3(pos)
        self.rotation = rot
        self.op = openning #oppening is an angle in radians

    def move(self, v):
        if type(v)==tuple:
            v = Vector3(v)
        v.rotateX(-self.rotation[1])
        v.rotateY(-self.rotation[0])
        self.position += v
    def rotate(self, a=(0,0)):
        r = self.rotation
        self.rotation = (r[0]+a[0],r[1]+a[1])

    def ttt(self, o=(0,0,0), te = False):
        p = self.relativePos(o)
        d = math.tan(self.op/2)*p.z
        #if d<0: d*=-1
        x = 0
        y = 0
        x = p.x*250.0/d+250
        y = p.y*-250.0/d+250
        return (x, y)

    def relativePos(self, o):
        p = Vector3((0,0,0))+o
        p -= self.position
        a = self.rotation
        p.rotateY(a[0])
        p.rotateX(a[1])
        return p

    def drawLine(self, a, b, te =False):
        p1 = Vector3(a)
        p2 = Vector3(b)
        pr1 = self.relativePos(p1)
        pr2 = self.relativePos(p2)
        if pr1.z < 0 and pr2.z > 0:
            x,y,z = 0,0,0
            if not p1.x == p2.x:
                x = pr2.x+pr2.z*(pr1.x-pr2.x)/(pr1.z+pr2.z)
            else:
                x = p1.x
            if not p1.y == p2.y:
                y = pr2.y+pr2.z*(pr1.y-pr2.y)/(pr1.z+pr2.z)
            else:
                y = p1.y
            p1 = self.ttt(Vector3((x, y, self.position.z+0.1)))
            p2 = self.ttt(p2)

        elif pr2.z < 0 and pr1.z > 0:
            if not p1.x == p2.x:
                m = (p2.z-p1.z)/(p2.x-p1.x)
                n = p1.z-m*p1.x
                x = (n+math.tan(self.rotation.x)*self.position.x)/(math.tan(self.rotation.x)-m)
            else:
                x = p2.x
            if not p1.y == p2.y:
                m = (p2.z-p1.z)/(p2.y-p1.y)
                n = p2.z-m*p1.y
                y = (n+math.tan(self.rotation.y)*self.position.y)/(math.tan(self.rotation.y)-m)
            else:
                y = p2.y
            p2 = self.ttt(Vector3((x, y, p2.z)))
            p1 = self.ttt(p1)


        elif pr1.z>0 and pr2.z>0:
            p1 = self.ttt(pr1)
            p2 = self.ttt(pr2)

        if p1 != p2 and not(pr1.z<0 and pr2.z<0):
            try:
                pygame.draw.line(screen, (255,255,255), p1, p2)
            except Exception as e:
                print(p1,p2)
                print(e)
                global running
                running = False
                


c =  Camera()
#GameObject((0, 0, 30),(0,0), (50, 10, 2))
#GameObject((0, 0, 40),(0,0), (50, 10, 2))
#GameObject((0, 5, 35),(0,0), (50, 2, 10))
GameObject((0,0, 30))
running = True

while running:
    screen.fill((0,0,0))
    GameObject.drawAll(c)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys=pygame.key.get_pressed()
    v = 0.01
    a = 0.001
    if keys[pygame.K_d]:
        c.move((v, 0, 0))
    if keys[pygame.K_a]:
        c.move((-v, 0, 0))
    if keys[pygame.K_w]:
        c.move((0, 0, v))
    if keys[pygame.K_s]:
        c.move((0, 0, -v))
    if keys[pygame.K_RIGHT]:
        c.rotate((-a,0))
    if keys[pygame.K_LEFT]:
        c.rotate((a,0))
    if keys[pygame.K_UP]:
        c.rotate((0,a))
    if keys[pygame.K_DOWN]:
        c.rotate((0, -a))
    if keys[pygame.K_LSHIFT]:
        c.move((0, v, 0))
    if keys[pygame.K_LCTRL]:
        c.move((0, -v, 0))
    pygame.display.update()
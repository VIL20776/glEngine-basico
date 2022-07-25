import struct
from collections import namedtuple

V2 = namedtuple('Point2', ['x', 'y'])

def char(c):
    #1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    #2 bytes
    return struct.pack('=h', w)

def dword(d):
    #4 bytes
    return struct.pack('=l', d)

def color(r, g, b):
    return bytes([
        int(b * 255),
        int(g * 255),
        int(r * 255)])

class Renderer(object):
    def __init__(self, width, height):
        self.glInit(width, height)

    def glInit(self, width, height):
        self.glCreateWindow(width, height)
        self.clearColor = color(0, 0, 0)
        self.currColor = color(1, 1, 1)
        self.fillColor = color(1, 1, 0)

        self.glClear()

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height

    def glViewport(self, posX, posY, width, height):
        self.vpX = posX
        self.vpY = posY
        self.vpWidth = width
        self.vpHeight = height
        
    def glClearColor(self, r, g, b):
        self.clearColor = color(r, g, b)

    def glClear(self):
        self.pixels = [[self.clearColor for y in range(self.height)]
            for x in range(self.width)]

    def glClearViewport(self, clr = None):
        for x in range(self.vpX, self.vpX + self.vpWidth):
            for y in range(self.vpY, self.vpY + self.vpHeight):
                self.glPoint(x,y,clr)
    
    def glColor(self, r, g, b):
        self.currColor = color(r, g, b)

    def glPoint(self, x, y, clr=None):
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[x][y] = clr or self.currColor
            return  
        
    def glVPoint(self, ndcX, ndcY, clr = None): # NDC
        if (ndcX < -1 or ndcX > 1) or (ndcY < -1 or ndcY > 1):
            print("Punto fuera del Viewport")
            return

        x = int((ndcX + 1) * (self.vpWidth / 2) + self.vpX)
        y = int((ndcY + 1) * (self.vpHeight / 2) + self.vpY)

        self.glPoint(x, y, clr)

    def glFillPoly(self, poly, clr=None):
        for y in range(self.height):
            for x in range(self.width):
                if self.EstaenRuta(x, y, poly):
                    self.pixels[x][y] = clr or self.fillColor

    # Algoritmo obtenido de https://es.wikipedia.org/wiki/Regla_par-impar
    def EstaenRuta(self, x, y, poly):
        '''
        x, y -- x e y coordenadas del punto
        poly -- una lista de tuplas [(x, y), (x, y), ...]
        '''
        num = len(poly)
        j = num - 1
        c = False
        for i in range(num):
                if  ((poly[i][1] > y) != (poly[j][1] > y)) and \
                        (x < (poly[j][0] - poly[i][0]) * (y - poly[i][1]) / (poly[j][1] - poly[i][1]) + poly[i][0]):
                    c = not c
                j = i
        return c
    
    def glLine(self, v0, v1, clr = None):
        # Bresenham line algorithm
        # y = m * x + b
        x0 = int(v0.x)
        x1 = int(v1.x)
        y0 = int(v0.y)
        y1 = int(v1.y)

        # Si el punto0 es igual al punto 1, dibujar solamente un punto
        if x0 == x1 and y0 == y1:
            self.glPoint(x0,y0,clr)
            return

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx

        # Si la linea tiene pendiente mayor a 1 o menor a -1
        # intercambio las x por las y, y se dibuja la linea
        # de manera vertical
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        # Si el punto inicial X es mayor que el punto final X,
        # intercambio los puntos para siempre dibujar de 
        # izquierda a derecha       
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        offset = 0
        limit = 0.5
        m = dy / dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                # Dibujar de manera vertical
                self.glPoint(y, x, clr)
            else:
                # Dibujar de manera horizontal
                self.glPoint(x, y, clr)

            offset += m

            if offset >= limit:
                if y0 < y1:
                    y += 1
                else:
                    y -= 1
                
                limit += 1

    def glFinish(self, filename):
        with open(filename, "wb") as file:
            #Header
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
            file.write(dword(14 + 40 + (self.height * self.width * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))

            #InfoHeader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.width))
            file.write(word(1))
            file.write(word(24)) 
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            #Color Table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])


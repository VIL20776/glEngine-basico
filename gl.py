import struct

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
    def __init__(self):
        self.glInit()

    def glInit(self):
        self.glCreateWindow(512, 512)
        self.clearColor = color(0, 0, 0)
        self.currColor = color(1, 1, 1)

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
        print("Punto fuera de la Ventana")    
        
    def glVPoint(self, ndcX, ndcY, clr = None): # NDC
        if (ndcX < -1 or ndcX > 1) or (ndcY < -1 or ndcY > 1):
            print("Punto fuera del Viewport")
            return

        x = int((ndcX + 1) * (self.vpWidth / 2) + self.vpX)
        y = int((ndcY + 1) * (self.vpHeight / 2) + self.vpY)

        self.glPoint(x, y, clr)

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


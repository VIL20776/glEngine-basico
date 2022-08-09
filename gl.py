import struct
from obj import Obj
from libAL import Matrix, matrixMult
from collections import namedtuple

import random

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z', 'w'])

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

def baryCoords(A, B, C, P):

    areaPBC = (B.y - C.y) * (P.x - C.x) + (C.x - B.x) * (P.y - C.y)
    areaPAC = (C.y - A.y) * (P.x - C.x) + (A.x - C.x) * (P.y - C.y)
    areaABC = (B.y - C.y) * (A.x - C.x) + (C.x - B.x) * (A.y - C.y)

    try:
        # PBC / ABC
        u = areaPBC / areaABC
        # PAC / ABC
        v = areaPAC / areaABC
        # 1 - u - v
        w = 1 - u - v
    except:
        return -1, -1, -1
    else:
        return u, v, w

class Renderer(object):
    def __init__(self, width, height):
        self.glInit(width, height)

    def glInit(self, width, height):
        self.glCreateWindow(width, height)
        self.clearColor = color(0, 0, 0)
        self.currColor = color(1, 1, 1)
        self.fillColor = color(1, 1, 0)
        self.activeShader = None
        self.active_texture = None
        self.dirLight = V3(0,0,1)
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
    
    def glCreateObjectMatrix(self, translate = V3(0,0,0), rotate = V3(0,0,0), scale = V3(1,1,1)):

        translation = Matrix(4, 4, matrix=[[1, 0, 0, translate.x],
                                        [0, 1, 0, translate.y],
                                        [0, 0, 1, translate.z],
                                        [0, 0, 0, 1]])

        rotation = Matrix(4,4)
        rotation.identity()

        scaleMat = Matrix(4, 4, matrix=[[scale.x, 0, 0, 0],
                                    [0, scale.y, 0, 0],
                                    [0, 0, scale.z, 0],
                                    [0, 0, 0, 1]])
        M1 = matrixMult(rotation, scaleMat)
        M2 = matrixMult(translation, M1)
        return M2

    def glTransform(self, vertex, matrix):

        v = Matrix(4, 1, [[vertex[0]], 
                            [vertex[1]],
                            [vertex[2]],
                            [1]])
        vt = matrixMult(matrix, v)
        vf = V3(vt.matrix[0][0]/ vt.matrix[3][0],
                vt.matrix[1][0]/ vt.matrix[3][0],
                vt.matrix[2][0]/ vt.matrix[3][0])

        return vf



    def glLoadModel(self, filename, translate = V3(0,0,0), rotate = V3(0,0,0), scale = V3(1,1,1)):
        model = Obj(filename)
        modelMatrix = self.glCreateObjectMatrix(translate, rotate, scale)

        for face in model.faces:
            vertCount = len(face)

            v0 = model.vertices[ face[0][0] - 1]
            v1 = model.vertices[ face[1][0] - 1]
            v2 = model.vertices[ face[2][0] - 1]

            v0 = self.glTransform(v0, modelMatrix)
            v1 = self.glTransform(v1, modelMatrix)
            v2 = self.glTransform(v2, modelMatrix)



            self.glTriangle_std(v0, v1, v2, color(random.random(),
                                                  random.random(),
                                                  random.random()))

    def glTriangle_std(self, A, B, C, clr = None):
        
        if A.y < B.y:
            A, B = B, A
        if A.y < C.y:
            A, C = C, A
        if B.y < C.y:
            B, C = C, B

        self.glLine(A,B, clr)
        self.glLine(B,C, clr)
        self.glLine(C,A, clr)

        def flatBottom(vA,vB,vC):
            try:
                mBA = (vB.x - vA.x) / (vB.y - vA.y)
                mCA = (vC.x - vA.x) / (vC.y - vA.y)
            except:
                pass
            else:
                x0 = vB.x
                x1 = vC.x
                for y in range(int(vB.y), int(vA.y)):
                    self.glLine(V2(x0, y), V2(x1, y), clr)
                    x0 += mBA
                    x1 += mCA

        def flatTop(vA,vB,vC):
            try:
                mCA = (vC.x - vA.x) / (vC.y - vA.y)
                mCB = (vC.x - vB.x) / (vC.y - vB.y)
            except:
                pass
            else:
                x0 = vA.x
                x1 = vB.x
                for y in range(int(vA.y), int(vC.y), -1):
                    self.glLine(V2(x0, y), V2(x1, y), clr)
                    x0 -= mCA
                    x1 -= mCB

        if B.y == C.y:
            # Parte plana abajo
            flatBottom(A,B,C)
        elif A.y == B.y:
            # Parte plana arriba
            flatTop(A,B,C)
        else:
            # Dibujo ambos tipos de triangulos
            # Teorema de intercepto
            D = V2( A.x + ((B.y - A.y) / (C.y - A.y)) * (C.x - A.x), B.y)
            flatBottom(A,B,D)
            flatTop(B,D,C)

    def glTriangle_bc(self, A, B, C, texCoords = (), normals = (), clr = None):
        # bounding box
        minX = round(min(A.x, B.x, C.x))
        minY = round(min(A.y, B.y, C.y))
        maxX = round(max(A.x, B.x, C.x))
        maxY = round(max(A.y, B.y, C.y))

        triangleNormal = np.cross( np.subtract(B, A), np.subtract(C,A))
        # normalizar
        triangleNormal = triangleNormal / np.linalg.norm(triangleNormal)


        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                u, v, w = baryCoords(A, B, C, V2(x, y))

                if 0<=u and 0<=v and 0<=w:

                    z = A.z * u + B.z * v + C.z * w

                    if 0<=x<self.width and 0<=y<self.height:
                        if z < self.zbuffer[x][y]:
                            self.zbuffer[x][y] = z

                            if self.active_shader:
                                r, g, b = self.active_shader(self,
                                                                baryCoords=(u,v,w),
                                                                vColor = clr or self.currColor,
                                                                texCoords = texCoords,
                                                                normals = normals,
                                                                triangleNormal = triangleNormal)



                                self.glPoint(x, y, color(r,g,b))
                            else:
                                self.glPoint(x,y, clr)

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


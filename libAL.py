from math import sqrt
from collections import namedtuple
V3 = namedtuple('Point3', ['x', 'y', 'z'])
class Matrix (object):
    def __init__(self, rows, columns, matrix=None):
        self.rows = rows
        self.columns = columns
        self.matrix = matrix or [[0 for x in range(self.columns)] for y in range(self.rows)]

    def identity(self):
        for y in range(self.rows):
            for x in range(self.columns):
                self.matrix[y][x] = 1 if (x == y) else 0

def matrixMult(matrix1, matrix2):
    if (matrix1.columns != matrix2.rows):
        return

    result = Matrix(matrix1.rows, matrix2.columns)

    for i in range(matrix2.columns):
        for y in range(matrix1.rows):
            value = 0
            for x in range(matrix1.columns):
                value += matrix1.matrix[y][x] * matrix2.matrix[x][i]
            result.matrix[y][i] = value
    
    return result

def subsVectors(v1, v2):
    return V3(v1.x - v2.x, v1.y - v2.y, v1.z - v1.z)

def cross (v1, v2):
    x = (v1.y * v2.z) - (v1.z * v2.y)
    y = (v1.x * v2.z) - (v1.z * v2.x)
    z = (v1.x * v2.y) - (v1.y * v2.x)
    return V3(x, y, z)

def normalize (vector):
    magnitude = sqrt(vector.x**2 + vector.y**2 + vector.z**2)
    return V3(vector.x/magnitude, vector.y/magnitude, vector.z/magnitude)

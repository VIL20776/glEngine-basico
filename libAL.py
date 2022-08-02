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

        

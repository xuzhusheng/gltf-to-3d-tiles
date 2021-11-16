import numpy as np
import math


class Matrix4:
    def __init__(self, elements=[1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], order="F") -> None:
        self.__order = order
        self.__matrix = np.array(elements).reshape(4, 4, order=order)

    @property
    def matrix(self):
        return self.__matrix

    @property
    def list(self):
        return self.__matrix.reshape(-1, order=self.__order).tolist()

    @property
    def position(self):
        return self.__matrix[0:3, 3].tolist()

    @property
    def inverse(self):
        return Matrix4(np.linalg.inv(self.__matrix).reshape(-1, order=self.__order).tolist())

    @property
    def __normal_matrix(self):
        return np.transpose(np.linalg.inv(self.__matrix[0:3, 0:3])) * self.scale

    @property
    def up(self):
        return self.__normal_matrix[0:3, 1].tolist()

    @property
    def right(self):
        return self.__normal_matrix[0:3, 0].tolist()

    @property
    def determinant(self):
        return np.linalg.det(self.__matrix)

    @property
    def scale(self):
        sx = math.sqrt(((self.__matrix[0:3, 0] ** 2).sum()))
        sy = math.sqrt(((self.__matrix[0:3, 1] ** 2).sum()))
        sz = math.sqrt(((self.__matrix[0:3, 2] ** 2).sum()))

        # if determine is negative, we need to invert one scale
        if np.linalg.det(self.__matrix) < 0:
            sx = -sx

        return [sx, sy, sz]

    def clone(self):
        return Matrix4(self.__matrix)

    def multiply(self, matrix):
        self.__matrix = self.__matrix @ matrix.matrix
        return self

    def premultiply(self, matrix):
        self.__matrix = matrix.matrix @ self.__matrix
        return self

    @property
    def is_identity(self):
        return (self.__matrix == Matrix4().matrix).all()

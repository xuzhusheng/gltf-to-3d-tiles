import math
import numpy as np


class Box3:
    def __init__(self, min=[math.inf] * 3, max=[-math.inf] * 3) -> None:
        self.__min = np.array(min)
        self.__max = np.array(max)

    def expand_by_point(self, point):
        self.__max = np.maximum(self.__max, point)
        self.__min = np.minimum(self.__min, point)
        return self

    @property
    def center(self):
        return ((self.__max + self.__min) / 2).tolist()

    @property
    def min(self):
        return self.__min

    @property
    def max(self):
        return self.__max

    @property
    def diagonal(self):
        size = self.size
        return math.sqrt(size[0] ** 2 + size[1] ** 2 + size[2] ** 2)

    @property
    def size(self):
        return abs(self.__max - self.__min)

    @property
    def list(self):
        half_size = abs(self.__max - self.__min) / 2
        return self.center + [half_size[0], 0, 0, 0, half_size[1], 0, 0, 0, half_size[2]]

    def union(self, box):
        self.__max = np.maximum(self.__max, box.max)
        self.__min = np.minimum(self.__min, box.min)
        return self

    def contains(self, box):
        return (self.__min <= box.min).all() and (
            box.max <= self.__max).all()

    def clone(self):
        return Box3(self.__min, self.__max)

    def clear(self):
        self.__min = np.array([math.inf] * 3)
        self.__max = np.array([-math.inf] * 3)

    def apply_matrix4(self, matrix):
        points = [[*self.__min, 1],
                  [self.__min[0], self.__min[1], self.__max[2], 1],
                  [self.__min[0], self.__max[1], self.__min[2], 1],
                  [self.__min[0], self.__max[1], self.__max[2], 1],
                  [self.__max[0], self.__min[1], self.__min[2], 1],
                  [self.__max[0], self.__min[1], self.__max[2], 1],
                  [self.__max[0], self.__max[1], self.__min[2], 1],
                  [*self.__max, 1]]
        self.clear()
        for point in points:
            self.expand_by_point((matrix @ point)[0:3])
        return self

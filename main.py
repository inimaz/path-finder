import numpy as np
import random

cells_number = 7


"""
We are going to show the following path finding algorithms:
Dijkstra’s Algorithm
A* Search Algorithm
D* Algorithm
"""


class Full_field():
    def __init__(self):
        self.__start_field()
        self.__set_obstacles()
        self.__set_origin_destination(1, 1, cells_number, cells_number)
        print(self.values)

    def __start_field(self):
        self.values = np.zeros((cells_number, cells_number))
        self.solved = np.zeros((cells_number, cells_number))

    def __set_obstacles(self, number_of_obstacles=cells_number):
        _ = 0
        while _ < number_of_obstacles:
            i = random.randint(0, cells_number - 1)
            j = random.randint(0, cells_number - 1)
            self.values[i, j] = -1
            _ += 1

    def __set_origin_destination(self, x0, y0, xf, yf):
        self.solved[x0, y0] = 1

    def check(self):

        for i in range(cells_number):
            for j in range(cells_number):
                if self.solved[i, j]:
                    self.find_next_node(i, j)

        for i in range(cells_number):
            for j in range(cells_number):
            	if self.solved[i, j] == -1:
            		self.solved[i, j] = 0

    def find_next_node(self, x0, y0):
        for i in [x0 - 1, x0, x0 + 1]:
            for j in [y0 - 1, y0, y0 + 1]:
                if i >= 0 & i < cells_number \
                        & j >= 0 & i < cells_number:
                    x1 = i
                    y1 = j
                    self.__set_value(x0, y0, x1, y1)



    def __set_value(self, x0, y0, x1, y1):
        distance = ((x1 - x0) ^ 2 + (y1 - y0) ^ 2) ^ (1 / 2)
        cumulative_distance = self.values[x0, y0] + distance
        if self.solved[x1, y1] == 0 | \
                (self.solved[x1, y1] == -1 & cumulative_distance < self.values[x1, y1]):
            self.values[x1, y1] = cumulative_distance
            self.solved[x1, y1] = -1


Full_field()

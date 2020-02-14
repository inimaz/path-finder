import numpy as np
import random

cells_number = 10


"""
We are going to show the following path finding algorithms:
Dijkstra’s Algorithm
A* Search Algorithm
D* Algorithm
"""


class Full_field():
    def __init__(self):
        '''
        Status:
        1 = solved
        0 = not visited
        -1 = to be checked next
        -2 = Obstacle
        3 = shortest path
        '''
        self.__start_field()
        print(self.status)
        print(self.values)

    def __start_field(self):
        self.values = np.zeros((cells_number, cells_number))
        self.status = np.zeros((cells_number, cells_number))
        self.previous_cell = np.full(
            (cells_number, cells_number), tuple)

    def set_obstacles(
            self, obstacle_positions=[], number_of_obstacles=cells_number):
        """
        Obstacles will be flagged as cells of value -2
        """
        if obstacle_positions == []:
            _ = 0
            while _ < number_of_obstacles:
                i = random.randint(0, cells_number - 1)
                j = random.randint(0, cells_number - 1)
                if self.status[i, j] != 1:
                    self.status[i, j] = -2
                _ += 1
        else:
            for pos in obstacle_positions:
                if self.status[pos] != 1:
                    self.status[pos] = -2

    def set_origin_destination(
            self, x0=0, y0=0, xf=cells_number - 1, yf=cells_number - 1
    ):
        self.x0 = x0
        self.y0 = y0
        self.xf = xf
        self.yf = yf

        self.status[x0, y0] = 1
        self.status[xf,yf] = 2

    def find_shortest_path(self):
        while self.status[self.xf, self.yf] != 1:
            self.check_nodes()
            print('These are the values\n', self.values)
            print('This is to see which one is solved\n', self.status)

    def check_nodes(self):

        for i in range(cells_number):
            for j in range(cells_number):
                if self.status[i, j] == 1:
                    self.find_next_node(i, j)
        print("These are the candidates'status\n", self.status)

        # Search the closest node with the minimum value
        node_values = []
        node_pos = []
        for i in range(cells_number):
            for j in range(cells_number):
                if self.status[i, j] == -1:
                    self.status[i, j] = 0
                    node_values.append(self.values[i, j])
                    node_pos.append([i, j])
        print(node_values)
        pos = np.argmin(node_values)
        closest_node = tuple(node_pos[pos])
        print('Node to be set as solved', closest_node)

        self.status[closest_node] = 1

    def find_next_node(self, x0, y0):
        for i in [x0 - 1, x0, x0 + 1]:
            for j in [y0 - 1, y0, y0 + 1]:
                if (i >= 0) & (i < cells_number) \
                        & (j >= 0) & (j < cells_number):
                    x1 = int(i)
                    y1 = int(j)
                    self.__set_value(x0, y0, x1, y1)

    def __set_value(self, x0, y0, x1, y1):
        distance = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** (1 / 2)
        cumulative_distance = self.values[x0, y0] + distance
        if (self.status[x1, y1] in [0,2]) | \
                (self.status[x1, y1] == -1 &
                 (cumulative_distance < self.values[x1, y1])):
            self.values[x1, y1] = cumulative_distance
            self.status[x1, y1] = -1
            self.previous_cell[x1, y1] = (x0, y0)

    def show_path(self):
        print(self.previous_cell)
        x = self.xf
        y = self.yf

        while (x != self.x0) | (y != self.y0):
            self.status[x, y] = 3
            x, y = self.previous_cell[x, y]

        print("This is the shortest path from ", self.x0, self.y0,
              "to", self.xf, self.yf, "\n", self.status)


class Find_Path(Full_field):
    def __init__(self):
        Full_field.__init__(self)
        self.set_origin_destination()
        self.set_obstacles()
        self.find_shortest_path()
        self.show_path()


if __name__ == "__main__":
    Find_Path()

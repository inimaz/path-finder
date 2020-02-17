import numpy as np
import random
import logging
import logging.config

logging.config.fileConfig('logging.conf')

# create logger
logger = logging.getLogger('simpleExample')


# Setting the size of the field
cells_number = 15


"""
We are going to show the following path finding algorithms:
Dijkstra’s Algorithm algorithm = D
A* Search Algorithm algorithm = A*
D* Algorithm algorithm = D*
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
        self.algorithm = "A*"
        self.__start_field()
        logger.info('Starting status of the board \n:' + str(self.status))
        logger.info('Starting distance values\n' + str(self.values))

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
                if self.status[i, j] not in [1, 2]:
                    self.status[i, j] = -2
                _ += 1
        else:
            for pos in obstacle_positions:
                if self.status[pos] != 1:
                    self.status[pos] = -2

    def set_origin(
            self, x0=0, y0=0):
        self.x0 = x0
        self.y0 = y0

        self.status[x0, y0] = 1

    def set_destination(
            self, xf=cells_number - 1, yf=cells_number - 1
    ):

        self.xf = xf
        self.yf = yf

        self.status[xf, yf] = 2

    def select_algorithm(self, algorithm):
        """
        We are going to show the following path finding algorithms:
                Dijkstra’s Algorithm algorithm = Di
                A* Search Algorithm algorithm = A*
                D* Algorithm algorithm = D*
        """
        self.algorithm = algorithm

    def find_shortest_path(self):
        while self.status[self.xf, self.yf] != 1:
            self.check_nodes()
            self.min_closest_node()
            logger.info('These are the values\n' + str(self.values))
            logger.info('This is to see which one is solved\n' +
                        str(self.status))

    def check_nodes(self):

        for i in range(cells_number):
            for j in range(cells_number):
                if self.status[i, j] == 1:
                    self.find_next_node(i, j)
        logger.info("These are the candidates'status\n" + str(self.status))

    def min_closest_node(self):
        # Search the closest node with the minimum value
        node_values = []
        node_pos = []
        for i in range(cells_number):
            for j in range(cells_number):
                if self.status[i, j] == -1:
                    self.status[i, j] = 0
                    node_values.append(self.values[i, j])
                    node_pos.append([i, j])
        logger.debug('This is the minimum value: ' + str(node_values))
        try:
            pos = np.argmin(node_values)
        except:
            logger.error('It is not possible to go from ' + str(self.x0) + str(self.y0) +
                         " to " + str(self.xf) + str(self.yf))
        closest_node = tuple(node_pos[pos])
        logger.debug('Node to be set as solved' + str(closest_node))

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
        distance_to_origin = self.__distance_between(x0, y0, x1, y1)
        if self.algorithm == "A*":
            distance_to_destination_x0 = self.__distance_between(
                x0, y0, self.xf, self.yf)
            distance_to_destination = self.__distance_between(
                x1, y1, self.xf, self.yf)
        elif self.algorithm == "Di":
            distance_to_destination = distance_to_destination_x0 = 0
        cumulative_distance = self.values[x0, y0] - distance_to_destination_x0 + \
            distance_to_origin + distance_to_destination
        if (self.status[x1, y1] in [0, 2]) or \
                ((self.status[x1, y1] == -1) and
                 (cumulative_distance < self.values[x1, y1])):
            self.values[x1, y1] = cumulative_distance
            self.status[x1, y1] = -1
            self.previous_cell[x1, y1] = (x0, y0)

    def __distance_between(self, x0, y0, x1, y1):
        distance = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** (1 / 2)
        return distance

    def show_path(self):
        logger.debug('This is the previous_cell\n' + str(self.previous_cell))
        x = self.xf
        y = self.yf

        while (x != self.x0) | (y != self.y0):
            self.status[x, y] = 3
            if x == self.xf and y == self.yf:
                self.status[x, y] = 2
            x, y = self.previous_cell[x, y]

        logger.info("This is the shortest path from " + str(self.x0) + str(self.y0) +
                    " to " + str(self.xf) + str(self.yf) + "\n" + str(self.status))

    def solve_fast(self):
        self.find_shortest_path()
        self.show_path()

    def solve_one_step(self):
        if self.status[self.xf, self.yf] != 1:
            self.check_nodes()


class Find_Path(Full_field):
    def __init__(self):
        Full_field.__init__(self)
        self.set_origin()
        self.set_destination()
        self.set_obstacles()
        self.solve_fast()


if __name__ == "__main__":
    Find_Path()

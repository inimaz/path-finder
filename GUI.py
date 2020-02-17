from tkinter import Tk, Canvas, Frame, Label, Button, BOTH, TOP, BOTTOM, LEFT, RIGHT
from main import Full_field, cells_number
import time

MARGIN = 20  # Pixels around the board
SIDE = 30  # Width of every board cell.
# Width and height of the whole board
WIDTH = HEIGHT = MARGIN * 2 + SIDE * cells_number


class StartUI:
    def __init__(self, master):
        # Initialize values
        self.selected_column = -1
        self.selected_row = -1
        self.x0, self.y0, self.xf, self.yf = -1, -1, -1, -1

        self.Field = Full_field()
        self.master = master
        master.title("Path finder")

        # Initialize the GUI
        try:
            self.canvas.destroy()
        except:
            pass

        self.canvas = Canvas(master, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack(fill=BOTH, side=BOTTOM)

        self.frame = Frame(master)
        self.frame.pack(side=TOP)

        self.canvas.bind("<Button-1>", self.canvas_click)
        self.__draw_box()

    def __set_origin_destination(self):
        if self.x0 == -1 and self.y0 == -1:
            self.label = Label(
                self.frame, text="Please, select the origin")
            self.label.pack(side=TOP)
            if self.selected_row != -1 and self.selected_column != -1:
                self.x0 = self.selected_row
                self.y0 = self.selected_column
                self.Field.set_origin(self.x0, self.y0)
                self.selected_row = -1
                self.selected_column = -1
                self.label.config(text="Please, select the destination")

        if self.xf == -1 and self.yf == -1 and \
                self.selected_row != -1 and self.selected_column != -1:
            self.xf = self.selected_row
            self.yf = self.selected_column
            self.Field.set_destination(self.xf, self.yf)
            self.selected_row = -1
            self.selected_column = -1
            self.label.config(text="Select where to put your obstacles")

            self.start_button = Button(
                self.master, text="Find the shortest path",
                fg='green', command=self.__start_path_finding)
            self.start_button.pack(side=BOTTOM)

        self.__draw_box()

    def __start_path_finding(self):
        self.label.config(text="Finding the shortest path...")
        self.start_button.config(text="Restart", command=self.__init__(self.master))
        if self.Field.status[self.xf, self.yf] != 1:
            self.Field.solve_one_step()
            self.__draw_box()
            self.Field.min_closest_node()
            self.__draw_box()
            self.canvas.after(200, self.__start_path_finding)
        else:
            self.Field.show_path()
            self.__draw_box()

    def __draw_obstacles(self):
        if self.selected_row != -1 and self.selected_column != -1:
            self.Field.set_obstacles(obstacle_positions=[(
                self.selected_row, self.selected_column)])

    def __draw_box(self):
        '''
        Draw status:
        2 = end of the path
        1 = solved
        0 = not visited
        -1 = to be checked next
        -2 = Obstacle
        3 = shortest path
        '''
        for row in range(0, cells_number):
            for column in range(0, cells_number):
                if self.Field.status[row, column] == 0:
                    color = "white"
                elif self.Field.status[row, column] == 1:
                    color = "light grey"
                elif self.Field.status[row, column] == 2:
                    color = "yellow"
                elif self.Field.status[row, column] == -1:
                    color = "purple"
                elif self.Field.status[row, column] == -2:
                    color = "black"
                elif self.Field.status[row, column] == 3:
                    color = "green"
                x0 = MARGIN + row * SIDE + 1
                y0 = MARGIN + column * SIDE + 1
                x1 = MARGIN + (row + 1) * SIDE - 1
                y1 = MARGIN + (column + 1) * SIDE - 1
                self.canvas.create_rectangle(
                    x0, y0, x1, y1, fill=color, outline="black", tags="cells")
        if self.x0 != -1 and self.y0 != -1:
            x0 = MARGIN + self.x0 * SIDE + 1
            y0 = MARGIN + self.y0 * SIDE + 1
            x1 = MARGIN + (self.x0 + 1) * SIDE - 1
            y1 = MARGIN + (self.y0 + 1) * SIDE - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1, outline="red")

        if self.xf != -1 and self.yf != -1:
            x0 = MARGIN + self.xf * SIDE + 1
            y0 = MARGIN + self.yf * SIDE + 1
            x1 = MARGIN + (self.xf + 1) * SIDE - 1
            y1 = MARGIN + (self.yf + 1) * SIDE - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1, outline="green")
        self.__draw_distance_value()

    def canvas_click(self, event):
        '''
        Selects which cell has been clicked
        '''
        x, y = event.x, event.y
        if WIDTH - MARGIN > x > MARGIN and HEIGHT - MARGIN > y > MARGIN:
            self.canvas.focus_set()

            row = (x - MARGIN) // SIDE
            column = (y - MARGIN) // SIDE

            self.selected_row, self.selected_column = row, column

        self.__set_origin_destination()
        if self.xf != -1 and self.yf != -1:
            self.__draw_obstacles()
        self.__draw_box()
        self.__draw_selected_box()

    def __draw_selected_box(self):
        '''
        Draw red box around the cell selected
        '''
        self.canvas.delete("purple_square")
        if self.selected_row >= 0 and self.selected_column >= 0:
            x0 = MARGIN + self.selected_row * SIDE + 1
            y0 = MARGIN + self.selected_column * SIDE + 1
            x1 = MARGIN + (self.selected_row + 1) * SIDE - 1
            y1 = MARGIN + (self.selected_column + 1) * SIDE - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1, outline="purple", tags="purple_square")

    def __draw_distance_value(self):
        for i in range(0, cells_number):
            for j in range(0, cells_number):
                number = self.Field.values[i, j]
                if number != 0:
                    number = "{:.1f}".format(number)
                    x = MARGIN + SIDE / 2 + i * SIDE
                    y = MARGIN + SIDE / 2 + j * SIDE
                    self.canvas.create_text(
                        x, y, text=number, tags="numbers", fill="black")


if __name__ == "__main__":
    root = Tk()
    StartUI(root)
    root.mainloop()

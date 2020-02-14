from tkinter import Tk, Canvas, Frame, Label, Button, BOTH, TOP, BOTTOM, LEFT, RIGHT
from main import Full_field
cells_number = 10
MARGIN = 20  # Pixels around the board
SIDE = 30  # Width of every board cell.
# Width and height of the whole board
WIDTH = HEIGHT = MARGIN * 2 + SIDE * cells_number


class StartUI:
    def __init__(self, master):
        self.master = master
        master.title("Path finder")
        self.canvas = Canvas(master, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack(fill=BOTH, side=TOP)

        self.frame = Frame(master)
        self.frame.pack(side=TOP)

        self.start_button = Button(
            master, text="Find the shortest path", fg='purple')
        self.start_button.pack(side=BOTTOM)

        # Initiialize values
        self.selected_column = -1
        self.selected_row = -1
        self.x0, self.y0, self.xf, self.yf = -1, -1, -1, -1

        self.canvas.bind("<Button-1>", self.canvas_click)

        self.Field = Full_field()
        self.__draw_box()
        # self.__draw_obstacles()

    def __set_origin_destination(self):
        self.label = Label(
            self.frame, text="Please, select the origin")
        self.label.pack(side=TOP)
        if self.x0 == -1 and self.y0 == -1 and\
                self.selected_row != -1 and self.selected_column != -1:
            self.x0 = self.selected_row
            self.y0 = self.selected_column
            self.selected_row = -1
            self.selected_column = -1

        self.label.config(text="Please, select the destination")

        if self.xf == -1 and self.yf == -1 and \
                self.selected_row != -1 and self.selected_column != -1:
            self.xf = self.selected_row
            self.yf = self.selected_column
            self.Field.set_origin_destination(self.x0, self.y0, self.xf, self.yf)
            self.selected_row = -1
            self.selected_column = -1
        self.__draw_box()

    def __draw_main_grid(self):
        self.__draw_box()

        self.canvas.after(200, self.__draw_main_grid)

    def __draw_box(self):
        '''
        Draw red box around the cell selected
                Status:
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
                    color = "blue"
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
        self.__draw_selected_box()


    def __draw_selected_box(self):
        '''
        Draw red box around the cell selected
        '''
        self.canvas.delete("red_square")
        if self.selected_row >= 0 and self.selected_column >= 0:
            x0 = MARGIN + self.selected_row * SIDE + 1
            y0 = MARGIN + self.selected_column * SIDE + 1
            x1 = MARGIN + (self.selected_row + 1) * SIDE - 1
            y1 = MARGIN + (self.selected_column + 1) * SIDE - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1, outline="red", tags="red_square")


if __name__ == "__main__":
    root = Tk()
    StartUI(root)
    root.mainloop()

import tkinter as tk

class Board:
    def __init__(self, root):
        self.width = 1220
        self.height = 320

        self.board_width = 1200
        self.board_height = 300
        self.n_columns = 60
        self.n_rows = 15

        self.sq_width = self.board_width / self.n_columns
        self.sq_height = self.board_height / self.n_rows

        #Build the board
        self.canvas = tk.Canvas(root, width=self.width, height=self.height)
        self.canvas.pack()
        self.draw_board()
    
    #Draw all squares onto board
    def draw_board(self):
        for x in range(self.n_columns):
            x0 = (x*self.sq_width) + 10
            for y in range(self.n_rows):
                y0 = (y*self.sq_height) + 10
                #x0, y0, x1, y1
                self.canvas.create_rectangle(x0, y0, (x0+self.sq_width), (y0+self.sq_height), fill="black", outline='grey')
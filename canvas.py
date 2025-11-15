import tkinter as tk
import pandas as pd
import numpy as np

class Board:
    def __init__(self, root):
        self.width = 1620
        self.height = 320

        self.board_width = 1600
        self.board_height = 300
        self.n_columns = 80
        self.n_rows = 15

        self.empty = True

        self.sq_width = self.board_width / self.n_columns
        self.sq_height = self.board_height / self.n_rows

        self.letters = self.get_csv('resources/letters.csv')

        #Build the board
        self.board = []
        self.canvas = tk.Canvas(root, width=self.width, height=self.height)
        self.canvas.pack()
        self.draw_board()

    
    #Draw all squares onto board
    def draw_board(self):
        for y in range(self.n_rows):
            y0 = (y*self.sq_height) + 10
            row = []
            for x in range(self.n_columns):
                x0 = (x*self.sq_width) + 10
                #x0, y0, x1, y1
                row.append(self.canvas.create_rectangle(x0, y0, (x0+self.sq_width), (y0+self.sq_height), fill="black", outline='grey'))
            self.board.append(row)
            # board = [ [row0], 
            #           [row1],
            #           [row2]
            #           .....
            #         ] 
            # (length = 15)

    def change_background(self):
        for item in self.board[0]:
            self.canvas.itemconfig(item, fill='red')

    def write_c(self):
        for i in range(9, 20):
            self.canvas.itemconfig(self.board[1][i], fill='#FF9A2E')
            self.canvas.itemconfig(self.board[2][i], fill='#FF9A2E')
        for i in range(2, 13):
            self.canvas.itemconfig(self.board[i][9], fill='#FF9A2E')
            self.canvas.itemconfig(self.board[i][10], fill='#FF9A2E')
        for i in range(9, 20):
            self.canvas.itemconfig(self.board[13][i], fill='#FF9A2E')
            self.canvas.itemconfig(self.board[12][i], fill='#FF9A2E')
        
        self.empty = False


    def clear_board(self):
        if self.empty:
            return
        for item in self.board:
            for sq in item:
                self.canvas.itemconfig(sq, fill='black')
        self.empty = True

    def get_csv(self, file_path):
        return pd.read_csv(file_path, dtype=str)


    def draw_letter(self, letter: str):
        letter_row = self.letters.loc[self.letters['letter'] == letter]
        if(letter_row.empty):
            print(f'The {letter} key has not been implemented yet.')
        else:
            letter_binary = letter_row['box_on'].values[0]
            box = letter_row['box'].values[0].split("*")
            width = int(box[0])
            height = int(box[1])

            i = 0
            y0 = 3
            for y in range(height):
                x0 = 30
                for x in range(width):
                    if(letter_binary[i] == '1'):
                        self.canvas.itemconfig(self.board[y0+y][x0+x], fill='#FF9A2E')
                    i += 1
            self.empty = False

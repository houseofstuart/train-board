import tkinter as tk
import pandas as pd
from announcement import Announcement

class Board:
    def __init__(self, root, cols, rows):
        self.width = 1420
        self.height = 320

        self.board_width = 1400
        self.board_height = 300
        self.n_columns = cols
        self.n_rows = rows

        self.empty = True

        self.sq_width = self.board_width / self.n_columns
        self.sq_height = self.board_height / self.n_rows

        #Build the board
        self.board = []
        self.canvas = tk.Canvas(root, width=self.width, height=self.height)
        self.canvas.pack()
        self.draw_board()


    def display_data(self, board_array):
        self.clear_board()
        for x, column in enumerate(board_array):
            for y, value in enumerate(column):
                if value == 1:
                    self.canvas.itemconfig(self.board[y][x], fill='#FF9A2E')
        self.empty = False

    def clear_board(self):
        if self.empty:
            return
        for item in self.board:
            for sq in item:
                self.canvas.itemconfig(sq, fill='black')
        self.empty = True


    
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




    def draw_letter(self, letter: str):
        self.clear_board()
        letter_row = self.letters.loc[self.letters['letter'] == letter]
        if(letter_row.empty):
            print(f'The {letter} key has not been implemented yet.')
        else:
            letter_binary = letter_row['box_on'].values[0]
            box = letter_row['box'].values[0].split("*")
            letter_width = int(box[0])
            letter_height = int(box[1])

            i = 0
            y0 = self.n_rows - letter_height
            x0 = self.n_columns - 4

            width = letter_width
            if (x0 + width) >= 70:
                width = self.n_columns - x0

            for y in range(letter_height):
                for x in range(width):
                    if(letter_binary[(y * letter_width) + x] == '1'):
                        self.canvas.itemconfig(self.board[y0+y][x0+x], fill='#FF9A2E')
                    i += 1
            self.empty = False

    def display_announcement(self, announcement: Announcement):
        self.clear_board()
        letter_row = self.letters.loc[self.letters['letter'] == announcement.text]
        if(letter_row.empty):
            print(f'The {announcement.text} key has not been implemented yet.')
            return
        
        box = letter_row['box'].values[0].split("*")
        letter_data = {
            'binary': letter_row['box_on'].values[0],
            'width': int(box[0]),
            'height': int(box[1])
        }

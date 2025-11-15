import tkinter as tk
import time
from queue import Queue
from canvas import Board



def handle_key(event):
    board.clear_board()
    board.draw_letter(event.char)

root = tk.Tk()
root.title("Announcements")

board = Board(root=root)

root.bind("<Key>", handle_key)
root.mainloop()




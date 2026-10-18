import tkinter as tk
import queue
from canvas import Board
from announcement import Announcement

board_queue = queue.Queue()

def handle_key(event):
    board.clear_board()
    board.draw_letter(event.char)

def read_entry():
    text = input_variable.get()
    if text != "":
        board_queue.put(text)
        entry.delete(0, tk.END)

def queue_worker(root, board):
    try:
        item = board_queue.get_nowait()
        anc = Announcement(item, False)
        board.draw_letter(anc.text[0])
    except queue.Empty:
        pass
    root.after(100, queue_worker, root, board)

root = tk.Tk()
root.title("Announcements")

board = Board(root=root)
win_b = tk.Toplevel(root)
win_b.title("Entry")
input_variable = tk.StringVar()
entry = tk.Entry(win_b, width=30, textvariable=input_variable)
entry.pack()
button = tk.Button(win_b, width=5, height=1, text="Submit", command=read_entry)
button.pack()


root.bind("<Key>", handle_key)
root.after(100, queue_worker, root, board)
root.mainloop()




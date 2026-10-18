import tkinter as tk
import numpy as np
import queue, threading, time
from canvas import Board
from announcement import Announcement

from manager import Manager

def read_entry(input, entry, queue):
    text = input.get()
    if text != "":
        #Create announcement and enqueue it
        new_announcement = Announcement(text, True)
        queue.put(new_announcement)
        entry.delete(0, tk.END)

def announcement_worker(announcement_queue: queue, board):
    current_ann = None
    board_manager = Manager(np.zeros((70, 15)))
    while True:
        # Update current announcement when one doesn't exist
        if current_ann is None:
            try:
                current_ann = announcement_queue.get()
                board_manager.set_announcement(current_ann)
                board_manager.reset_clock()
                # board_manager.static_display()
                board_manager.start_display()
            except queue.Empty:
                pass
        else:
            board_manager.tick()
            board.display_data(board_manager.get_board_array())
            if board_manager.get_ended_status():
                current_ann = None
        time.sleep(0.05)


def main():
    root = tk.Tk()
    root.title("ANNOUNCEMENT BOARD")

    board = Board(root=root, cols=70, rows=15)
    board_array = np.zeros((70, 15)) #array[0] = first column (len=15)
    announcement_queue = queue.Queue()

    input_window = tk.Toplevel(root)
    input_window.title("Announcement Entry")
    input_variable = tk.StringVar()
    input_entry = tk.Entry(input_window, width=30, textvariable=input_variable)
    input_entry.pack()

    input_button = tk.Button(input_window, width=5, height=1, text='Submit', command=lambda: read_entry(input_variable, input_entry, announcement_queue))
    input_button.pack()

    #Create thread to manage announcement
    t2 = threading.Thread(target=announcement_worker, args=(announcement_queue, board), daemon=True)
    t2.start()
    root.mainloop()
 

#Main run
if __name__ == "__main__":
    main()
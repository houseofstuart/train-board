import tkinter as tk
from tkinter import ttk
import numpy as np
import queue, threading, time
from canvas import Board
from announcement import Announcement

from manager import Manager

def read_entry(input, movement, entry, queue):
    text = input.get()
    if text != "":
        #Create announcement and enqueue it
        movement = movement.get()
        static = True if movement == "Static" else False
        new_announcement = Announcement(text, static)
        queue.put(new_announcement)
        entry.delete(0, tk.END)

def add_announcement():
    pass

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
                if current_ann.static:
                    board_manager.static_display()
                else:
                    board_manager.start_display()
            except queue.Empty:
                pass
        else:
            board_manager.tick()
            board.display_data(board_manager.get_board_array())
            if board_manager.get_ended_status():
                current_ann = None
        time.sleep(0.05)

def update_queue_display(root, queue, queue_list):
    with queue.mutex:
        items = list(queue.queue)

    queue_list.delete(0, tk.END)
    for item in items:
        queue_list.insert(tk.END, item.text)

    root.after(100, update_queue_display, root, queue, queue_list)


def main():
    root = tk.Tk()
    root.title("Announcements")
    board = Board(root=root, cols=70, rows=15)

    announcement_queue = queue.Queue()

    #Testing
    control_window = tk.Toplevel(root)
    control_window.title("Control Window")
    control_window.geometry("800x600")

    control_window.grid_columnconfigure(0, weight=1, uniform="equal")
    control_window.grid_columnconfigure(1, weight=1, uniform="equal")
    control_window.grid_rowconfigure(0, weight=1)

    input_frame = tk.Frame(control_window)
    input_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    input_variable = tk.StringVar()
    input_entry = tk.Entry(input_frame, textvariable=input_variable)
    input_entry.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

    notebook = ttk.Notebook(input_frame)
    notebook.pack(side=tk.TOP, expand=True, fill=tk.BOTH, padx=10, pady=5)

    options_tab = tk.Frame(notebook)
    options_var = tk.StringVar(value="Moving")
    for tool in ["Moving", "Static", "Blinking"]:
        tk.Radiobutton(
            options_tab,
            text=tool,
            variable=options_var,
            value=tool
        ).pack(anchor="w", padx=20, pady=5)

    notebook.add(options_tab, text="Options")


    input_button = tk.Button(
        input_frame,
        text='Submit',
        command=lambda: read_entry(input_variable, options_var, input_entry,  announcement_queue)
    )
    input_button.pack(side=tk.TOP, expand=False, fill=tk.X, padx=10, pady=10)

    queue_frame = tk.Frame(control_window, bg="skyblue")
    queue_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    queue_list = tk.Listbox(queue_frame, bg="skyblue")
    queue_list.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    update_queue_display(root, announcement_queue, queue_list)



    #Create thread to manage announcement
    t2 = threading.Thread(target=announcement_worker, args=(announcement_queue, board), daemon=True)
    t2.start()
    root.mainloop()
 

#Main run
if __name__ == "__main__":
    main()
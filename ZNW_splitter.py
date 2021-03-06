import tkinter as tk
from tkinter import messagebox, END, PhotoImage, Entry, Button, Label
from tkinter.filedialog import askopenfile, askdirectory
from tkinter import ttk
from threading import Thread
import threading
import extract_personnel_pdfs
from logger import get_logger


LOGGER = get_logger("Frontend")

window = tk.Tk()

window.geometry("800x500")
window.configure(bg="#ffffff")
canvas = tk.Canvas(
    window,
    bg="#ffffff",
    height=500,
    width=800,
    bd=0,
    highlightthickness=0,
    relief="ridge",
)
canvas.place(x=0, y=0)
window.resizable(False, False)
window.title("ZNW-Splitter | Version 0.1.0")

# Title
# title = canvas.create_text(
#     131.0, 51.0, text="ZNW-Splitter", fill="#000000", font=("Roboto", int(30.0))
# )

# Logo
logo_img = PhotoImage(file=f"files/logo.png").subsample(2)
logo_field = canvas.create_image(655, 51, image=logo_img)

# instructions
open_instructions = canvas.create_text(
    230,
    130.0,
    text="Select a Timesheet-PDF to split by employee:",
    fill="#000000",
    font=("Roboto", int(16.0)),
)

save_instructions = canvas.create_text(
    130,
    225.0,
    text="Select a path to save to:",
    fill="#000000",
    font=("Roboto", int(16.0)),
)

# File-Explorer-Boxes
open_img = PhotoImage(file=f"files/io_image.png")
open_field = canvas.create_image(297.0, 170.0, image=open_img)

open_entry = Entry(
    window,
    bg="#e5e5e5",
    bd=0,
    fg="black",
    highlightthickness=0,
    font=("Roboto", int(12.0)),
)

open_entry.place(x=25.0, y=145, width=544.0, height=50)

save_img = PhotoImage(file=f"files/io_image.png")
save_field = canvas.create_image(297.0, 265.0, image=save_img)

save_entry = Entry(
    bd=0,
    bg="#e5e5e5",
    fg="black",
    highlightthickness=0,
    font=("Roboto", int(12.0)),
)

save_entry.place(x=25.0, y=240, width=544.0, height=50)

info_text = Label(
    text="", bg="white", fg="black", justify="left", font=("Roboto", int(12.0))
)
info_text.place(x=20.0, y=340.0)

# Buttons
open_button_image = PhotoImage(file=f"files/open_button.png")
open_button = Button(
    image=open_button_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: open_file(),
    relief="flat",
)

open_button.place(x=594, y=145, width=188, height=50)

save_button_image = PhotoImage(file=f"files/save_button.png")
save_button = Button(
    image=save_button_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: save_path_btn(),
    relief="flat",
)

save_button.place(x=594, y=240, width=188, height=50)

run_button_image = PhotoImage(file=f"files/run_button.png")
run_button = Button(
    image=run_button_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: Thread(target=run_program).start(),
    relief="flat",
)

run_button.place(x=594, y=425, width=188, height=50)

# Render Progressbar
pb = ttk.Progressbar(
    window,
    style="success.Horizontal.TProgressbar",
    orient="horizontal",
    mode="determinate",
    length=544,
)
pb.place(x=20, y=450)


# ProgressBar
def set_progressbar(queue_pb, queue_pb_max):
    max_queue = queue_pb_max.get()
    pb["maximum"] = max_queue
    queue_current = queue_pb.get()

    while max_queue > queue_current:
        print(max_queue, queue_current)
        pb["value"] = queue_current
        queue_current = queue_pb.get()

    pb["value"] = max_queue


def open_file():
    LOGGER.info(f"open file dialog")
    pb["value"] = 0
    info_text.config(text="")
    open_entry.delete(0, END)
    file = askopenfile(
        parent=window,
        mode="rb",
        title="Choose a file",
        filetypes=[("Pdf file", "*.pdf")],
    )
    if file:
        open_entry.insert(0, file.name)
        LOGGER.info(f"open_file: {file.name}")
    else:
        LOGGER.debug(f"open_file canceled.")


def save_path_btn():
    LOGGER.info(f"save file dialog")
    pb["value"] = 0
    info_text.config(text="")
    save_entry.delete(0, END)
    filepath = askdirectory()
    if filepath:
        save_entry.insert(0, filepath)
        LOGGER.info(f"save_path: {filepath}")
    else:
        LOGGER.debug(f"save_file canceled.")


# Getting errors from threads
def excepthook(args):
    LOGGER.debug(f"{str(args)}")
    info_text.config(
        text=f"Splitting ZNW was not successful. :( \n Check errors in log-file.",
        fg="#E95454",
    )

    raise Exception("Error in Thread. :(")


threading.excepthook = excepthook


def run_program():
    run_button["state"] = "disabled"
    window.config(cursor="wait")
    pb["value"] = 0
    LOGGER.info(f"running...")
    info_text.config(text="")
    input_file = open_entry.get()
    out_path = save_entry.get()

    if input_file == "":
        LOGGER.info(f"input file path is empty.")
        tk.messagebox.showwarning(
            "No file selected!",
            "Please select a time sheet file which you would like to split!",
        )
        window.config(cursor="")
        run_button["state"] = "normal"
        return

    if out_path == "":
        LOGGER.info(f"save file path is empty.")
        tk.messagebox.showwarning(
            "No save-path selected!", "Please choose save folder."
        )
        window.config(cursor="")
        run_button["state"] = "normal"
        return

    try:
        pb_thread = Thread(
            target=set_progressbar,
            args=(extract_personnel_pdfs.queue_pb, extract_personnel_pdfs.queue_pb_max),
        )
        pb_thread.start()
        split_pdfs = Thread(
            target=extract_personnel_pdfs.open_pdf, args=(input_file, out_path)
        )
        split_pdfs.start()
        split_pdfs.join()
        pb_thread.join()
        info_text.config(text=f"Splitting ZNW successfully carried out.", fg="#46B546")
        window.config(cursor="")
        run_button["state"] = "normal"
        LOGGER.info(f"pdf successfully splitted.")
    except Exception as e:
        LOGGER.debug(f"{str(e)}")
        info_text.config(
            text=f"Splitting ZNW was not successful. :( \n Check errors in log-file.",
            fg="#E95454",
        )
        window.config(cursor="")
        run_button["state"] = "normal"


window.mainloop()

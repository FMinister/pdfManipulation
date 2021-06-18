import tkinter as tk
from tkinter import messagebox, END, PhotoImage, Entry, Button, Label
from tkinter.filedialog import askopenfile, askdirectory
from tkinter import ttk
from threading import Thread
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
window.title("ZNW-Splitter")

# Title
title = canvas.create_text(
    131.0, 51.0, text="ZNW-Splitter", fill="#000000", font=("Roboto", int(30.0))
)

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
    bd=0,
    bg="#e5e5e5",
    fg="black",
    highlightthickness=0,
    font=("Roboto", int(12.0)),
    state="disabled",
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
    state="disabled",
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

run_button.place(x=594, y=335, width=188, height=50)

# ProgressBar
pb = ttk.Progressbar(
            window,
            orient='horizontal',
            mode='indeterminate',
            length=544
        )
pb.place(x=20, y=450)


def open_file():
    LOGGER.info(f"open file dialog")
    info_text.config(text="")
    open_entry.configure(state="normal")
    open_entry.delete(0, END)
    file = askopenfile(
        parent=window,
        mode="rb",
        title="Choose a file",
        filetypes=[("Pdf file", "*.pdf")],
    )
    if file:
        open_entry.insert(0, file.name)
        open_entry.configure(state="disabled")
        LOGGER.info(f"open_file: {file.name}")
    else:
        open_entry.configure(state="disabled")
        LOGGER.debug(f"open_file canceled.")


def save_path_btn():
    LOGGER.info(f"save file dialog")
    info_text.config(text="")
    save_entry.configure(state="normal")
    save_entry.delete(0, END)
    filepath = askdirectory()
    if filepath:
        save_entry.insert(0, filepath)
        save_entry.configure(state="disabled")
        LOGGER.info(f"save_path: {filepath}")
    else:
        save_entry.configure(state="disabled")
        LOGGER.debug(f"save_file canceled.")


def run_program():
    LOGGER.info(f"running...")
    info_text.config(text="")
    input_file = open_entry.get()
    out_path = save_entry.get()
    pb.start(interval=10)
    if input_file == "":
        LOGGER.info(f"input file path is empty.")
        tk.messagebox.showwarning(
            "No file selected!",
            "Please select a time sheet file which you would like to split!",
        )
        return

    if out_path == "":
        LOGGER.info(f"save file path is empty.")
        tk.messagebox.showwarning(
            "No save-path selected!", "Please choose save folder."
        )
        return

    try:
        extract_personnel_pdfs.open_pdf(input_file, out_path)
        info_text.config(text="Splitting ZNW successfully carried out.", fg="#46B546")
        LOGGER.info(f"pdf successfully splitted.")
    except Exception as e:
        LOGGER.debug(f"{str(e)}")
        info_text.config(
            text=f"Splitting ZNW was not successful. :( \n Check errors in log-file.",
            fg="#E95454",
        )

    pb.stop()


window.mainloop()

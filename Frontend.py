import tkinter as tk
from tkinter import messagebox, END
from tkinter.filedialog import askopenfile, askdirectory
import textwrap
import extract_personnel_pdfs
from logger import get_logger


LOGGER = get_logger("Frontend")

root = tk.Tk()

_FILEPATHS = ["", ""]

canvas = tk.Canvas(root, width=650, height=300)
canvas.grid(columnspan=10, rowspan=9)
root.resizable(False, False)
root.title("ZNW-Splitter")
canvas.configure(background="#2B2B2B")

# instructions
instructions = tk.Label(
    root,
    text="Select a Timesheet-PDF to split by employee.",
    font="Helvetica 14 bold",
    bg="#2B2B2B",
    fg="#0092ff",
)
instructions.grid(columnspan=2, column=0, row=1)

# buttono
browse_text = tk.StringVar()
browse_btn = tk.Button(
    root,
    textvariable=browse_text,
    command=lambda: open_file(),
    font="Helvetica",
    bg="#0092ff",
    fg="white",
    height=2,
    width=15,
)
browse_text.set("Open...")
browse_btn.grid(column=8, row=2)

save_btn_text = tk.StringVar()
save_btn = tk.Button(
    root,
    textvariable=save_btn_text,
    command=lambda: save_path_btn(),
    font="Helvetica",
    bg="#0092ff",
    fg="white",
    height=2,
    width=15,
)
save_btn_text.set("Save to...")
save_btn.grid(column=8, row=3)

run_btn_text = tk.StringVar()
run_btn = tk.Button(
    root,
    textvariable=run_btn_text,
    command=lambda: run_program(),
    font="Helvetica",
    bg="#0092ff",
    fg="white",
    height=2,
    width=15,
)
run_btn_text.set("Run")
run_btn.grid(column=8, row=4)

text_box_open = tk.Text(root, width=55, height=2, padx=2, pady=2, bg="#9C9C9C")
text_box_open.grid(column=1, row=2)
text_box_save = tk.Text(root, width=55, height=2, padx=2, pady=2, bg="#9C9C9C")
text_box_save.grid(column=1, row=3)

lower_grid = tk.Label(
    root,
    text="",
    font="Helvetica 12 bold",
    bg="#2B2B2B",
    fg="#46B546",
)
lower_grid.grid(columnspan=2, column=0, row=4)


def open_file():
    LOGGER.info(f"open file dialog")
    lower_grid.config(text="")
    browse_text.set("loading...")
    file = askopenfile(
        parent=root, mode="rb", title="Choose a file", filetypes=[("Pdf file", "*.pdf")]
    )
    if file:
        _FILEPATHS[0] = file.name
        file_name = textwrap.wrap(file.name, 45)
        text_box_open.config(state="normal")
        text_box_open.delete("1.0", "end")
        text_box_open.insert(1.0, "\n".join(file_name))
        text_box_open.tag_configure("center", justify="center")
        text_box_open.tag_add("center", 1.0, "end")
        text_box_open.grid(column=1, row=2)
        text_box_open.config(state="disabled")
        LOGGER.info(f"open_file: {file_name}")
    else:
        LOGGER.debug(f"open_file canceled.")

    browse_text.set("Open...")


def save_path_btn():
    LOGGER.info(f"save file dialog")
    lower_grid.config(text="")
    save_btn_text.set("loading...")
    filepath = askdirectory()
    if filepath:
        _FILEPATHS[1] = filepath
        file_name = textwrap.wrap(filepath, 45)
        text_box_save.config(state="normal")
        text_box_save.delete("1.0", "end")
        text_box_save.insert(1.0, "\n".join(file_name))
        text_box_save.tag_configure("center", justify="center")
        text_box_save.tag_add("center", 1.0, "end")
        text_box_save.grid(column=1, row=3)
        text_box_save.config(state="disabled")
        LOGGER.info(f"save_path: {file_name}")
    else:
        LOGGER.debug(f"save_file canceled.")

    save_btn_text.set("Save to...")


def run_program():
    lower_grid.config(text="")

    LOGGER.info(f"running...")
    input_file = _FILEPATHS[0]
    out_path = _FILEPATHS[1]
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

    run_btn_text.set("Running...")
    try:
        extract_personnel_pdfs.open_pdf(input_file, out_path)
        lower_grid.config(text="Splitting ZNW successfully carried out.")
        LOGGER.info(f"pdf successfully splitted.")
    except Exception as e:
        LOGGER.debug(f"{str(e)}")
        lower_grid.config(text="Splitting ZNW was not successful. :( \n Error in log-file.")

    run_btn_text.set("Run")


root.mainloop()

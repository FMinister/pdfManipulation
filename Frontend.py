import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfile, askdirectory
import textwrap
import extract_personnel_pdfs

root = tk.Tk()

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


def open_file():
    browse_text.set("loading...")
    file = askopenfile(
        parent=root, mode="rb", title="Choose a file", filetypes=[("Pdf file", "*.pdf")]
    )
    if file:
        file_name = textwrap.wrap(file.name, 45)
        text_box_open.insert(1.0, "\n".join(file_name))
        text_box_open.tag_configure("center", justify="center")
        text_box_open.tag_add("center", 1.0, "end")
        text_box_open.grid(column=1, row=2)
        text_box_open.config(state="disabled")

    browse_text.set("Open...")


def save_path_btn():
    save_btn_text.set("loading...")
    filepath = askdirectory()
    if filepath:
        file_name = textwrap.wrap(filepath, 45)
        text_box_save.insert(1.0, "\n".join(file_name))
        text_box_save.tag_configure("center", justify="center")
        text_box_save.tag_add("center", 1.0, "end")
        text_box_save.grid(column=1, row=3)
        text_box_save.config(state="disabled")

    save_btn_text.set("Save to...")


def run_program():
    input_file = (text_box_open.get("1.0", "end-1c")).replace("\n", "")
    out_path = (text_box_save.get("1.0", "end-1c")).replace("\n", "")
    if input_file == "":
        tk.messagebox.showwarning(
            "No file selected!", "Please select a time sheet file which you would like to split!"
        )
        return

    if out_path == "":
        tk.messagebox.showwarning(
            "No save-path selected!", "Please choose save folder."
        )
        return

    run_btn_text.set("Running...")
    extract_personnel_pdfs.open_pdf(input_file, out_path)
    success = tk.Label(
        root,
        text="Splitting ZNW successfully carried out.",
        font="Helvetica 12 bold",
        bg="#2B2B2B",
        fg="#46B546",
    )
    success.grid(columnspan=2, column=0, row=4)
    run_btn_text.set("Run")


root.mainloop()

import tkinter as tk

VERSION = "0.1.0-alpha"
AUTHOR = "0xIkari"

def show_about(master):
    win = tk.Toplevel(master)
    win.title("About FoxxCAD")
    win.geometry("300x160")
    win.resizable(False, False)

    tk.Label(win, text="FoxxCAD", font=("Arial", 16, "bold")).pack(pady=(15, 5))
    tk.Label(win, text=f"Version: {VERSION}").pack()
    tk.Label(win, text=f"By: {AUTHOR}").pack()

    tk.Label(win, text="A lightweight 2D drafting tool.", fg="gray").pack(pady=(10, 0))
    tk.Label(win, text="https://github.com/nuclear-treestump/FoxCAD", fg="blue").pack()
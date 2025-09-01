import tkinter as tk
from .canvas.canvasview import CanvasView
from .engine.engineclass import DrawingEngine
from .config.config_ui import ConfigWindow, DEFAULT_COLORS
from .about import show_about

def main():
    import tkinter as tk

    root = tk.Tk()
    root.title("FoxxCAD")
    config = DEFAULT_COLORS.copy()
    engine = DrawingEngine()
    canvas = CanvasView(root, engine, config=config, bg=config["background"])
    canvas.pack(fill="both", expand=True)

    def open_config():
        ConfigWindow(root, config, on_apply=canvas.redraw)

    menubar = tk.Menu(root)
    config_menu = tk.Menu(menubar, tearoff=0)
    config_menu.add_command(label="Colors", command=open_config)
    menubar.add_cascade(label="Config", menu=config_menu)
    root.config(menu=menubar)
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="About", command=lambda: show_about(root))
    help_menu.add_separator()
    help_menu.add_command(label="Check for Updates", command=lambda: print("TODO: Check GitHub"))
    menubar.add_cascade(label="Help", menu=help_menu)

    root.mainloop()
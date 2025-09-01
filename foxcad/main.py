import tkinter as tk
import platform
from .canvas.canvasview import CanvasView
from .engine.engineclass import DrawingEngine
from .config.config_ui import ConfigWindow, DEFAULT_COLORS_DARK
from .profiles import profilemanager
from .about import show_about

def main():

    root = tk.Tk()
    root.title("FoxxCAD")
    root.geometry("1280x800") # Default size

    system = platform.system()
    if system == "Windows":
        root.state("zoomed")
    elif system == "Darwin":  # macOS
        root.attributes("-zoomed", True)
    elif system == "Linux":
        root.attributes("-zoomed", True) # Best effort

    profile_name = profilemanager.get_active_profile_name()
    def on_profile_loaded(profile_name):
        profilemanager.set_active_profile(profile_name)
        profile = profilemanager.load_profile(profile_name)
        config = DEFAULT_COLORS_DARK.copy()
        config.update(profile.get("colors", {}))
        launch_main_app(root, config, profile)

    if not profile_name:
        def on_profile_loaded(profile_name):
            profilemanager.set_active_profile(profile_name)
            profile = profilemanager.load_profile(profile_name)
            config = DEFAULT_COLORS_DARK.copy()
            config.update(profile.get("colors", {}))
            launch_main_app(root, config, profile)

        wizard = profilemanager.ProfileWizard(root, on_finish=on_profile_loaded)
        root.wait_window(wizard)  # BLOCK until wizard closes
    else:
        profile = profilemanager.load_profile(profile_name)
        config = DEFAULT_COLORS_DARK.copy()
        config.update(profile.get("colors", {}))
        launch_main_app(root, config, profile)

    root.mainloop()

def launch_main_app(root, config, profile):
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
import tkinter as tk
from tkinter import colorchooser

DEFAULT_COLORS_DARK = {
    "background": "#000000",
    "grid": "#444444",
    "line": "#ffffff",
    "dimension": "#00ffff",
    "constraint": "#ff00ff",
    "sketch_boundary": "#999999"
}

DEFAULT_COLORS_LIGHT = {
    "background": "#ffffff",
    "grid": "#dddddd",
    "line": "#000000",
    "dimension": "#0000ff",
    "constraint": "#ff00ff",
    "sketch_boundary": "#666666"
}

def get_contrast_color(hex_color):
    """Return black or white depending on background brightness."""
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    brightness = (r*299 + g*587 + b*114) / 1000  # perceptual brightness
    return 'black' if brightness > 128 else 'white'

class ConfigWindow(tk.Toplevel):
    def __init__(self, master, config, on_apply=None):
        super().__init__(master)
        self.transient(master)
        self.grab_set()
        self.lift()
        self.focus_force()
        self.title("Color Palette Configuration")
        self.config_ref = config
        self.on_apply = on_apply
        self.entries = {}

        for i, (key, color) in enumerate(config.items()):
            label = tk.Label(self, text=key.capitalize())
            label.grid(row=i, column=0, padx=10, pady=5)

            entry = tk.Entry(self)
            entry.insert(0, color)
            entry.grid(row=i, column=1, padx=10, pady=5)

            # Create button now, but delay setting color
            btn = tk.Button(self, text="Pick")
            btn.grid(row=i, column=2)
            btn.config(command=lambda k=key, e=entry, b=btn: self.choose_color(k, e, b))

            btn_dark = tk.Button(self, text="Reset: Dark Mode", command=self.reset_dark)
            btn_dark.grid(row=len(config)+1, column=0, columnspan=3, pady=(5, 0))

            
            btn_light = tk.Button(self, text="Reset: Light Mode", command=self.reset_light)
            btn_light.grid(row=len(config)+2, column=0, columnspan=3, pady=(0, 10))

            self.entries[key] = (entry, btn)
            self.update_button_color(btn, color)

        apply_btn = tk.Button(self, text="Apply", command=self.apply)
        apply_btn.grid(row=len(config), column=0, columnspan=3, pady=10)

    def update_button_color(self, button, hex_color):
        fg = get_contrast_color(hex_color)
        button.config(bg=hex_color, fg=fg)

    def choose_color(self, key, entry, button):
        color = colorchooser.askcolor(title=f"Choose {key} color")
        if color[1]:
            entry.delete(0, tk.END)
            entry.insert(0, color[1])
            self.update_button_color(button, color[1])

    def reset_dark(self):
        self.apply_theme(DEFAULT_COLORS_DARK)

    def reset_light(self):
        self.apply_theme(DEFAULT_COLORS_LIGHT)

    def apply_theme(self, theme_dict):
        for key, (entry, button) in self.entries.items():
            color = theme_dict.get(key)
            if color:
                entry.delete(0, tk.END)
                entry.insert(0, color)
                self.update_button_color(button, color)

    def apply(self):
        for key, (entry, _) in self.entries.items():
            self.config_ref[key] = entry.get()
        if self.on_apply:
            self.on_apply()
        self.destroy()
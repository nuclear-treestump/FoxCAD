import tkinter as tk
from tkinter import colorchooser

DEFAULT_COLORS = {
    "background": "#000000",
    "grid": "#444444",
    "line": "#ffffff",
    "dimension": "#00ffff",
    "constraint": "#ff00ff",
    "sketch_boundary": "#999999"
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

    def apply(self):
        for key, (entry, _) in self.entries.items():
            self.config_ref[key] = entry.get()
        if self.on_apply:
            self.on_apply()
        self.destroy()
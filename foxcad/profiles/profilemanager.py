import os
import sys
import json
import platform
import tkinter as tk
from tkinter import ttk, messagebox
import os

APP_NAME = "FoxxCAD"

class ProfileWizard(tk.Toplevel):
    def __init__(self, master, on_finish):
        super().__init__(master)
        self.title("FoxxCAD - First Time Setup")
        self.geometry("1200x800")
        self.resizable(True, True)
        self.transient(master)
        self.grab_set()
        self.on_finish = on_finish

        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="Welcome to FoxxCAD!", font=("Arial", 14, "bold")).pack(pady=(15, 5))
        tk.Label(self, text="Set up your user profile", font=("Arial", 10)).pack(pady=(0, 15))
        tk.Label(self, text="This information personalizes your FoxxCAD experience.\nProfiles store unit preferences, color schemes, author tags,\nand project folder defaults.", justify="left", fg="gray", font=("Arial", 9)).pack()

        frame = tk.Frame(self)
        frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Existing profiles
        profiles = list_profiles()
        self.profile_choice = tk.StringVar()
        if profiles:
            tk.Label(frame, text="Load Existing Profile:").grid(row=0, column=0, sticky="w")
            self.profile_dropdown = ttk.Combobox(frame, textvariable=self.profile_choice, values=profiles, state="readonly")
            self.profile_dropdown.grid(row=0, column=1, sticky="ew", pady=5)
        else:
            self.profile_dropdown = None

        # Name
        tk.Label(frame, text="Profile Name:").grid(row=1, column=0, sticky="w")
        tk.Label(frame, text="(Unique name for this profile. Spaces, special characters, and punctuation will be removed.)", wraplength=360, justify="left", fg="gray").grid(row=1, column=2, sticky="w", padx=(5,0))
        self.name_entry = tk.Entry(frame)
        self.name_entry.grid(row=1, column=1, sticky="ew", pady=5)

        # Author
        tk.Label(frame, text="Author:").grid(row=2, column=0, sticky="w")
        tk.Label(frame, text="(Optional. Used for title blocks and metadata.)", wraplength=360, justify="left", fg="gray").grid(row=2, column=2, sticky="w", padx=(5,0))
        self.author_entry = tk.Entry(frame)
        self.author_entry.grid(row=2, column=1, sticky="ew", pady=5)

        # Email
        tk.Label(frame, text="Email:").grid(row=3, column=0, sticky="w")
        tk.Label(frame, text="(Optional. Used for title blocks and metadata, not transmitted to FoxxCAD dev)", wraplength=360, justify="left", fg="gray").grid(row=3, column=2, sticky="w", padx=(5,0))
        self.email_entry = tk.Entry(frame)
        self.email_entry.grid(row=3, column=1, sticky="ew", pady=5)

        # Units
        tk.Label(frame, text="Units:").grid(row=4, column=0, sticky="w")
        self.units_choice = tk.StringVar(value="inches")
        self.units_dropdown = ttk.Combobox(frame, textvariable=self.units_choice, values=["inches", "mm", "cm"], state="readonly")
        self.units_dropdown.grid(row=4, column=1, sticky="ew", pady=5)

        # Organization
        tk.Label(frame, text="Organization:").grid(row=5, column=0, sticky="w")
        tk.Label(frame, text="(Optional. Used for title blocks and metadata.)", wraplength=360, justify="left", fg="gray").grid(row=5, column=2, sticky="w", padx=(5,0))
        self.org_entry = tk.Entry(frame)
        self.org_entry.grid(row=5, column=1, sticky="ew", pady=5)

        # How Big Is Your Org
        tk.Label(frame, text="Organization Size:").grid(row=6, column=0, sticky="w")
        tk.Label(frame, text="(Optional. Not transmitted to FoxxCAD dev.)", wraplength=360, justify="left", fg="gray").grid(row=6, column=2, sticky="w", padx=(5,0))
        self.org_size_entry = tk.Entry(frame)
        self.org_size_entry.grid(row=6, column=1, sticky="ew", pady=5)

        # Do you want to transmit telemetry when reporting a bug?
        tk.Label(frame, text="Allow Telemetry with Bug Reports:").grid(row=7, column=0, sticky="w")
        tk.Label(frame, text="(Optional. Telemetry helps improve FoxxCAD but is not required. All reports are kept confidential.)", wraplength=360, justify="left", fg="gray").grid(row=7, column=2, sticky="w", padx=(5,0))
        self.telemetry_var = tk.BooleanVar(value=False)
        tk.Checkbutton(frame, variable=self.telemetry_var).grid(row=7, column=1, sticky="w")
        tk.Label(frame, text="This data includes some or all of the following:\n- Operating System\n- Hardware Configuration\n- User Preferences\n- Profile Name\n- Whether Cloud Connector was used\n- Version of Product\n- Last Operation\n- Processor Data, such as Memory Count for the application\n- Errors, if any", wraplength=360, justify="left", fg="gray").grid(row=8, column=1, sticky="w")
        tk.Label(frame, text="No personal data such as name, email, or organization is transmitted.", wraplength=360, justify="left", fg="gray").grid(row=9, column=1, sticky="w", pady=(0,10))
        tk.Label(frame, text="You can change this setting later in the Config menu.", wraplength=360, justify="left", fg="gray").grid(row=10, column=1, sticky="w", pady=(0,10))
        tk.Label(frame, text="Telemetry is disabled by default.", wraplength=360, justify="left", fg="gray").grid(row=11, column=1, sticky="w", pady=(0,10))
        tk.Label(frame, text="When submitting a bug report, you can choose to request an email update. This WILL be treated as consent to email you with any findings. \nThis will never be used for marketing or promotional purposes. Ever.\n\nIf you request email updates with a bug report, you'll receive a confirmation and can reply at any time to add more information or opt out. This is not an automated process, as it is run by a single developer.\n\nIf you prefer to not be contacted, you can always make an issue on GitHub.", wraplength=360, justify="left", fg="gray").grid(row=12, column=1, sticky="w", pady=(0,10))



        frame.columnconfigure(1, weight=1)

        # Action buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Use Selected", command=self.use_existing).pack(side="left", padx=5)
        tk.Button(button_frame, text="Create New", command=self.create_new).pack(side="left", padx=5)

    def use_existing(self):
        selected = self.profile_choice.get()
        if selected:
            self.on_finish(selected)
            self.destroy()
        else:
            messagebox.showwarning("No selection", "Please select a profile to load.")

    def create_new(self):
        name = self.name_entry.get().strip()
        author = self.author_entry.get().strip()
        units = self.units_choice.get().strip()

        if not name:
            messagebox.showwarning("Missing Info", "Profile name is required.")
            return

        profile = {
            "profile": name,
            "author": author or "Unknown",
            "units": units,
            "default_project_dir": os.path.expanduser("~/FoxxCAD_Projects"),
            "colors": {},
            "cloud": {
                "sync_enabled": False,
                "provider": None
            }
        }

        save_profile(name, profile)
        self.on_finish(name)
        self.destroy()

def get_home_dir():
    return os.path.expanduser("~")

def get_config_dir():
    system = platform.system()
    home = get_home_dir()

    if system == "Windows":
        return os.path.join(os.environ.get("APPDATA", home), APP_NAME)
    elif system == "Darwin":
        return os.path.join(home, "Library", "Application Support", APP_NAME)
    else:
        return os.path.join(home, ".config", APP_NAME)

def get_profile_dir():
    path = os.path.join(get_config_dir(), "profiles")
    os.makedirs(path, exist_ok=True)
    return path

def list_profiles():
    pdir = get_profile_dir()
    return [f[:-5] for f in os.listdir(pdir) if f.endswith(".json")]

def load_profile(name):
    path = os.path.join(get_profile_dir(), f"{name}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Profile '{name}' does not exist.")
    with open(path, "r") as f:
        return json.load(f)

def save_profile(name, data):
    path = os.path.join(get_profile_dir(), f"{name}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def set_active_profile(name):
    path = os.path.join(get_config_dir(), "active_profile.txt")
    with open(path, "w") as f:
        f.write(name)

def get_active_profile_name():
    path = os.path.join(get_config_dir(), "active_profile.txt")
    if os.path.exists(path):
        with open(path) as f:
            return f.read().strip()
    return None

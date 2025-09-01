import os
import sys
import platform

def get_config_path(app_name="FoxxCAD"):
    home = os.path.expanduser("~")
    system = platform.system()

    if system == "Windows":
        return os.path.join(os.environ.get("APPDATA", home), app_name)
    elif system == "Darwin":
        return os.path.join(home, "Library", "Application Support", app_name)
    else:  # Linux, Unix
        return os.path.join(home, ".config", app_name)

config_dir = get_config_path()
os.makedirs(config_dir, exist_ok=True)

# type: ignore

import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
import os
import shutil
import tempfile

# Default Mods folder path
DEFAULT_MODS_PATH = os.path.join(
    os.path.expanduser("~"),
    "Documentos",
    "Electronic Arts",
    "The Sims 4",
    "Mods"
)

# Main functions


def select_mod():
    path = filedialog.askopenfilename(
        title="Select the mod file (.zip)",
        filetypes=[("ZIP Files", "*.zip")]
    )
    mod_path_var.set(path)


def select_destination_folder():
    folder = filedialog.askdirectory(
        title="Select the destination folder for the mod"
    )
    destination_var.set(folder)


def install_mod():
    zip_path = mod_path_var.get()
    destination_folder = destination_var.get() or DEFAULT_MODS_PATH

    if not zip_path or not zip_path.endswith(".zip"):
        messagebox.showerror("Error", "Please select a valid .zip file.")
        return

    if not os.path.exists(zip_path):
        messagebox.showerror("Error", "Selected file does not exist.")
        return

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    if not os.access(destination_folder, os.W_OK):
        messagebox.showerror("Error", "Destination folder is not writable.")
        return

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            installed_files = []
            copy_errors = []

            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file.endswith(('.package', '.ts4script')):
                        source = os.path.join(root, file)
                        destination = os.path.join(destination_folder, file)

                        # Handle file overwrite
                        if os.path.exists(destination):
                            answer = messagebox.askyesno(
                                "Confirm", f"Do you want to overwrite {file}?"
                            )
                            if not answer:
                                continue  # Skip copying this file

                        try:
                            shutil.copy2(source, destination)
                            if os.path.exists(destination):
                                installed_files.append(file)
                            else:
                                copy_errors.append(file)
                        except Exception as e:
                            copy_errors.append(f"{file} - {str(e)}")

            if installed_files:
                msg = "Files installed:\n\n" + "\n".join(installed_files)
                if copy_errors:
                    msg += "\n\nErrors with:\n" + "\n".join(copy_errors)
                messagebox.showinfo("Installation Finished", msg)
            else:
                messagebox.showwarning(
                    "No Mod Installed",
                    "No valid files were found in the ZIP."
                )

    except Exception as e:
        messagebox.showerror("Error", f"Error installing the mod:\n{str(e)}")


# Interface
app = tk.Tk()
app.title("The Sims 4 Mod Installer")
app.geometry("500x300")
app.configure(bg="#F0F4F8")  # Soft background color

# Base styling
label_style = {"bg": "#F0F4F8", "fg": "#3C3C3C", "font": ("Arial", 12)}
entry_style = {"bg": "#E0E8F0", "fg": "#3C3C3C",
               "insertbackground": "#3C3C3C", "font": ("Arial", 10), "bd": 2}
button_style = {
    "bg": "#5A5A5A", "fg": "white",
    "activebackground": "#4A4A4A", "font": ("Arial", 10),
    "relief": "flat", "bd": 0, "padx": 15, "pady": 8, "width": 12, "height": 1
}


def on_hover(event, button):
    button.config(bg="#4A4A4A")


def on_leave(event, button):
    button.config(bg="#5A5A5A")


mod_path_var = tk.StringVar()
destination_var = tk.StringVar()

# Labels and Entries
tk.Label(app, text="Mod file (.zip) path:", **label_style).pack(pady=(15, 5))
tk.Entry(app, textvariable=mod_path_var, width=60,
         **entry_style).pack(pady=(5, 10))
select_file_button = tk.Button(
    app, text="Select File", command=select_mod, **button_style)
select_file_button.pack(pady=5)

tk.Label(app, text="Destination folder (Mods):", **label_style).pack(pady=5)
tk.Entry(app, textvariable=destination_var,
         width=60, **entry_style).pack(pady=(5, 10))
select_folder_button = tk.Button(
    app, text="Select Folder", command=select_destination_folder,
    **button_style
)
select_folder_button.pack(pady=5)

install_button = tk.Button(app, text="Install Mod",
                           command=install_mod, **button_style)
install_button.pack(pady=20)

# Adding hover effects
select_file_button.bind("<Enter>", lambda event,
                        button=select_file_button: on_hover(event, button))
select_file_button.bind("<Leave>", lambda event,
                        button=select_file_button: on_leave(event, button))
select_folder_button.bind("<Enter>", lambda event,
                          button=select_folder_button: on_hover(event, button))
select_folder_button.bind("<Leave>", lambda event,
                          button=select_folder_button: on_leave(event, button))
install_button.bind("<Enter>", lambda event,
                    button=install_button: on_hover(event, button))
install_button.bind("<Leave>", lambda event,
                    button=install_button: on_leave(event, button))

app.mainloop()

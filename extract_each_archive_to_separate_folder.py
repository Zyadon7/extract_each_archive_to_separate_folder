import os
import shutil
import tkinter as tk
from tkinter import filedialog
import zipfile
import lzma

# Open file dialog to select directory
root = tk.Tk()
root.withdraw()
directory = filedialog.askdirectory(title="Select Directory")

# Unzip all archives in the selected directory
for filename in os.listdir(directory):
    if filename.endswith(".zip"):
        archive_path = os.path.join(directory, filename)
        output_folder = os.path.splitext(archive_path)[0]
        os.makedirs(output_folder, exist_ok=True)
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(output_folder)
    elif filename.endswith(".7z"):
        archive_path = os.path.join(directory, filename)
        output_folder = os.path.splitext(archive_path)[0]
        os.makedirs(output_folder, exist_ok=True)
        with open(archive_path, 'rb') as file_ref:
            file_content = file_ref.read()
            with lzma.open(output_folder, 'wb') as output_file:
                output_file.write(file_content)

# Open the directory in File Explorer
if os.name == "nt":  # Windows OS
    os.startfile(directory)
elif os.name == "posix":  # Linux/Unix OS
    os.system(f"xdg-open {directory}")

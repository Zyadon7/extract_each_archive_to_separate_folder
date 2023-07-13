import os
import subprocess
import tkinter as tk
from tkinter import filedialog

# Open file dialog to select directory
root = tk.Tk()
root.withdraw()
directory = filedialog.askdirectory(title="Select Directory")

# PowerShell command to extract archives in the selected directory
powershell_command = f'''
$ErrorActionPreference = "Stop"
$files = Get-ChildItem -Path "{directory}" -File
foreach ($file in $files) {{
    $outputFolder = $file.FullName -replace "(\\.zip|\\.rar|\\.7z)$"
    Expand-Archive -Path $file.FullName -DestinationPath $outputFolder -Force
}}
'''

# Execute PowerShell command
try:
    subprocess.run(["powershell.exe", "-Command", powershell_command], check=True)
    print("Archives extracted successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error occurred while extracting archives: {e}")

# Open the directory in File Explorer
if os.name == "nt":  # Windows OS
    os.startfile(directory)

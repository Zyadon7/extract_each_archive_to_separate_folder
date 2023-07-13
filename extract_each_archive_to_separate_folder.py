import os
import subprocess
import tkinter as tk
from tkinter import filedialog

# Open file dialog to select directory
root = tk.Tk()
root.withdraw()
directory = filedialog.askdirectory(title="Select Directory")

# Set the path to the 7z executable
seven_zip_path = "C:\\path\\to\\7z.exe"  # Update with the actual path to 7z.exe

# PowerShell command to extract archives in the selected directory using 7z
powershell_command = f'''
$ErrorActionPreference = "Stop"
$files = Get-ChildItem -Path "{directory}" -File
foreach ($file in $files) {{
    $outputFolder = $file.FullName -replace "(\\.zip|\\.rar|\\.7z)$"
    if ($file.Extension -eq ".zip") {{
        Expand-Archive -Path $file.FullName -DestinationPath $outputFolder -Force
    }} elseif ($file.Extension -eq ".rar" -or $file.Extension -eq ".7z") {{
        & '{seven_zip_path}' e $file.FullName -o$outputFolder -y
    }}
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

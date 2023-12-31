import os
import subprocess
import tkinter as tk
from tkinter import filedialog

# Open file dialog to select directory
root = tk.Tk()
root.withdraw()
directory = filedialog.askdirectory(title="Select Directory")

# Set the path to the 7z executable
seven_zip_path = r"C:\Program Files\7-Zip\7z.exe"  # Update with the actual path to 7z.exe

# PowerShell command to extract archives in the selected directory using 7z
powershell_command = f'''
$ErrorActionPreference = "Stop"
$files = Get-ChildItem -Path "{directory}" -File
foreach ($file in $files) {{
    if ($file.Extension -eq ".zip") {{
        $outputFolder = Join-Path -Path "{directory}" -ChildPath $file.BaseName
        Expand-Archive -Path $file.FullName -DestinationPath $outputFolder -Force
    }} elseif ($file.Extension -eq ".rar") {{
        $outputFolder = Join-Path -Path "{directory}" -ChildPath $file.BaseName
        & '{seven_zip_path}' x -r -o$outputFolder $file.FullName
    }} elseif ($file.Extension -eq ".7z") {{
        $outputFolder = Join-Path -Path "{directory}" -ChildPath ($file.BaseNameWithoutExtension -replace '[^a-zA-Z0-9]', '_')
        $tempOutputFolder = $outputFolder
        $counter = 1
        while (Test-Path -Path $outputFolder) {{
            $outputFolder = Join-Path -Path "{directory}" -ChildPath "$tempOutputFolder$counter"
            $counter++
        }}
        cmd.exe /C "md `"$outputFolder`""
        & '{seven_zip_path}' x -r -o$outputFolder $file.FullName
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

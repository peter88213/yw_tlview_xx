"""language pack installer library module. 

Version @release

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/yw_tlview.xx
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from shutil import copytree
import zipfile
import os
import sys
from pathlib import Path
try:
    from tkinter import *
except ModuleNotFoundError:
    print('The tkinter module is missing. Please install the tk support package for your python3 version.')
    sys.exit(1)

APP = 'yw_tlview'

root = Tk()
processInfo = Label(root, text='')
message = []

pyz = os.path.dirname(__file__)


def extract_tree(sourceDir, targetDir):
    with zipfile.ZipFile(pyz) as z:
        for file in z.namelist():
            if file.startswith(f'{sourceDir}/'):
                z.extract(file, targetDir)


def cp_tree(sourceDir, targetDir):
    copytree(sourceDir, f'{targetDir}/{sourceDir}', dirs_exist_ok=True)


def output(text):
    message.append(text)
    processInfo.config(text=('\n').join(message))


def main(zipped=True):
    if zipped:
        copy_tree = extract_tree
    else:
        copy_tree = cp_tree

    scriptPath = os.path.abspath(sys.argv[0])
    scriptDir = os.path.dirname(scriptPath)
    os.chdir(scriptDir)

    # Open a tk window.
    root.geometry("600x150")
    root.title(f'Install language pack for {APP}')
    header = Label(root, text='')
    header.pack(padx=5, pady=5)

    # Prepare the messaging area.
    processInfo.pack(padx=5, pady=5)

    # Install the language pack.
    homePath = str(Path.home()).replace('\\', '/')
    applicationDir = f'{homePath}/.{APP}'
    if os.path.isdir(applicationDir):
        output('Copying locale ...')
        copy_tree('locale', applicationDir)
        output(f'Sucessfully installed the language pack at "{os.path.normpath(applicationDir)}"')
    else:
        output(f'ERROR: Cannot find a yw_tlview installation at "{applicationDir}"')

    root.quitButton = Button(text="Quit", command=quit)
    root.quitButton.config(height=1, width=30)
    root.quitButton.pack(padx=5, pady=5)
    root.mainloop()

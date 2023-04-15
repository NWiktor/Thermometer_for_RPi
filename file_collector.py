#!/usr/bin/env python3
# -*- coding: utf-8 -*-#

"""  Short summary

Libs
----

Help
----

Info
----
Wetzl Viktor - 2023.03.25 - All rights reserved
"""

import time
import os
import shutil


def main():
    """ Copy and rename all '.png' files in the starting directory
    to a subfolder named: 'database'.
    """
    files = []

    # List files
    for file in os.listdir(INITDIR):
        if file.endswith(".png"):
            files.append(file)

    if files is None:
        print("No '.png' found!")
        return

    # Create main folder
    try:
        os.mkdir(DATABASE_PATH)
        print(f"Folder created: {DATABASE_PATH}")

    except FileExistsError:
        print("Folder already exists!")

    # Copy and rename files
    for file in files:

        # Try block for folder creation
        try:
            basename = os.path.basename(file).split('.')[0]
            subdir = os.path.join(DATABASE_PATH, basename)
            os.mkdir(subdir)

        except FileExistsError:
            print(f"Folder already exist: {subdir}")

        # Try block for copy
        try:
            filename = f"{DATE}_{file}"
            src = os.path.join(INITDIR, file)
            dst = os.path.join(subdir, filename)
            shutil.copy2(src, dst)
            print(f"File copied: {filename}")

        except Exception as exc:
            print(exc)


if __name__ == '__main__':
    DATE = time.strftime("%Y-%m-%d", time.localtime())
    INITDIR = os.path.dirname(__file__)
    DATABASE_PATH = os.path.join(INITDIR, "database")
    main()

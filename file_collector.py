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

    # Create folder
    try:
        os.mkdir(DATABASE_PATH)
        print("Folder created")

    except FileExistsError:
        print("Folder already exists!")

    # Copy and rename files
    try:
        for file in files:
            filename = f"{DATE}_{file}"
            src = os.path.join(INITDIR, file)
            dst = os.path.join(DATABASE_PATH, filename)
            shutil.copy2(src, dst)

    except Exception as exc:
        print(exc)


if __name__ == '__main__':
    DATE = time.strftime("%Y-%m-%d", time.localtime())
    INITDIR = os.path.dirname(__file__)
    DATABASE_PATH = os.path.join(INITDIR, "database")
    main()

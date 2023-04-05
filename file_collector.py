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
import sys
import shutil


def main():
	files = []

	# List files
	for file in os.listdir():
		if file.endswith(".png"):
			files.append(file)

	if files is None:
		return

	# Create folder
	try:
		os.mkdir(DATABASE_PATH)

	except FileExistsError:
		print("Folder already exists!")

	# Copy and rename files
	for file in files:
		# filename = f"{DATE}_{file}"
		filename = "{0}_{1}".format(DATE, file)
		shutil.copy2(file, os.path.join(DATABASE_PATH, filename))


if __name__ == '__main__':
	DATE = time.strftime("%Y-%m-%d", time.localtime())
	INITDIR = os.path.dirname(__file__)
	DATABASE_PATH = os.path.join(INITDIR, "database")
	main()

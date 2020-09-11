# Imports the sys library, which will allow us to have access to 
# some variables maintained by the interpreter and to functions that
# interact strongly with the interpreter 

# --- https://docs.python.org/3/library/sys.html

import sys

# This script prints "Hello world!" to the terminal
# before showing the version information for this install of Python

print("Hello world!")
print("This is a Python script!\n")

print("=========================")
print("Python Version:")
print(sys.version)
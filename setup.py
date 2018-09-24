import os
from cx_Freeze import setup, Executable

base = None

executables = [Executable("main.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {
        'packages':packages,
    },
}
os.environ['TCL_LIBRARY'] = os.getcwd()+r'\lib\tcl8.6'
os.environ['TK_LIBRARY'] = os.getcwd()+r'\lib\tk8.6'

setup(
    name = "<any name>",
    options = options,
    version = "<any number>",
    description = '<any description>',
    executables = executables
)
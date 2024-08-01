import os
import subprocess

from common.config import ConfigData
from common.utils import Utils

# Learned how to get os.system output: https://www.geeksforgeeks.org/print-output-from-os-system-in-python/


class Colors:
    RED = "\x1b[31m"
    GRAY = "\x1b[90m"
    RESET = "\x1b[0m"


print(Utils.build_string(
    ConfigData.WINDOW_TITLE,
    "This is a terminal emulator for the IDE.",
    ""
))

# check if user is on windows
if os.name == "nt":
    print("\nWARNING: This entire project is built for Mac/Posix systems.\n")

while True:
    command = input(f"{Colors.GRAY}{os.getcwd()} >{Colors.RESET} ")

    os.system(command)
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        print(result)
    except subprocess.CalledProcessError as error:
        print(f"{Colors.RED}Error executing command: {error}")

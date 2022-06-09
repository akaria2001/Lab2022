import coloured_text
import subprocess as cmd
import time


def destroy_timer():
    for count in range(10, -1, -1):
        cmd.call("clear", shell=False)
        coloured_text.print_red(f"Destroying Lab in {count} seconds!!")
        time.sleep(1)

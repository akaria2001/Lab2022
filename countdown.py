import format_text
import subprocess as cmd
import time


def destroy_timer():
    for count in range(10, -1, -1):
        cmd.call("clear", shell=False)
        format_text.print_red(f"About to delete in {count} seconds!!")
        time.sleep(1)

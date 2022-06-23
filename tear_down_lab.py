#!/bin/python3
import subprocess as cmd
import getpass
import format_text
import lab_status
import check_instances_exist
import countdown


def generate_username():
    username = getpass.getuser()
    return username


def user_input():
    format_text.print_red("WARNING!!! About to delete all instances!!!")
    msg = '''

You will delete any existing instances,
Are you sure? - type 'yes' if you want to proceed :

'''

    confirmation = input(msg)
    return confirmation


def destroy():
    if(check_instances_exist.verify()):
        format_text.print_red("Instances found")
        lab_status.display()
        confirmation = user_input()
        if(confirmation == 'yes'):
            msg = f'''

            {generate_username()} has chosen {confirmation}:
            Instances will be deleted from the environment

            '''
            format_text.print_red(msg)
            countdown.destroy_timer()
            command = "lxc list -c n -f csv"
            output = cmd.check_output(command.split(), shell=False)
            output = output.decode('utf8')
            for entry in output.split("\n"):
                if(len(entry) <= 1):
                    continue
                destroy_command = f"lxc delete -f {entry}"
                format_text.print_red(f"Running command : {destroy_command}")
                cmd.call(destroy_command.split(), shell=False)
                lab_status.display()
    else:
        format_text.print_blue("No Instances found")


def main():
    cmd.call("clear", shell=False)
    destroy()


if __name__ == '__main__':
    main()

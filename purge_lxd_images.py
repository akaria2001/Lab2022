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
    format_text.print_warning("WARNING!!! About to delete all locally cached images!!")
    msg = '''

You will delete all locally cached images,
Are you sure? - type 'yes' if you want to proceed :

'''

    confirmation = input(msg)
    return confirmation


def destroy():
    confirmation = user_input()
    if(confirmation == 'yes'):
        msg = f'''

        {generate_username()} has chosen {confirmation}:
        Instances will be deleted from the environment

        '''
        format_text.print_red(msg)
        countdown.destroy_timer()
        command = "lxc image list -c f -f csv"
        output = cmd.check_output(command.split(), shell=False)
        output = output.decode('utf8')
        for entry in output.split("\n"):
            if(len(entry) <= 1):
                continue
            destroy_command = f"lxc image delete --debug {entry}"
            format_text.print_red(f"Running command : {destroy_command}")
            cmd.call(destroy_command.split(), shell=False)
    else:
        exit()


def main():
    cmd.call("clear", shell=False)
    destroy()


if __name__ == '__main__':
    main()

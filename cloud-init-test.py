import os

with open('user-data', 'r') as file:
    user_data = file.read()

command = f'lxc launch ubuntu:jammy my-test -p lab -c user.user-data="{user_data}"'
os.system(command)

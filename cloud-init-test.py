import subprocess

# Read the user-data file
with open('user-data', 'r') as file:
    user_data = file.read()

# Execute the command
subprocess.run(['lxc', 'launch', 'ubuntu:jammy', 'my-test3', '--config=user.user-data=' + user_data])
subprocess.run(['lxc', 'launch', 'ubuntu:jammy', 'my-test2', '--config=user.user-data='])

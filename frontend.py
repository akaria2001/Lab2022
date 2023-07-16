from flask import Flask, render_template
import subprocess as cmd

app = Flask(__name__)

def return_instances():
    instance_list = []
    command = "lxc list -c n -f csv"
    instances = cmd.check_output(command.split(), shell=False)
    instances = instances.decode('utf8')
    instance_list = instances.split()
    return instance_list


@app.route('/')
def index():
    return render_template('lab.html', instances=return_instances())

if __name__ == '__main__':
    app.run(port=20000)

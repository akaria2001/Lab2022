from flask import Flask, render_template
import subprocess as cmd

app = Flask(__name__)

def return_instances():
    instances = []
    command = "lxc list -c n -f csv"
    buffer = cmd.check_output(command.split(), shell=False)
    buffer = buffer.decode('utf8').split()
    instances.append(buffer)
    return instances

@app.route('/')
def index():
    return render_template('lab.html', instances=return_instances())

if __name__ == '__main__':
    app.run(port=20000)

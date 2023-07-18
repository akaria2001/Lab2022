from flask import Flask, render_template
import subprocess as cmd

app = Flask(__name__)

def return_instances():
    instance_list = []
    command = "lxc list -c n,s,t,image.os:OS,4 -f compact"
    instances = cmd.check_output(command.split(), shell=False)
    instances = instances.decode('utf8')
    instance_list = instances.split("\n")
    return instance_list


def return_instance_qty():
    instance_list = "lxc list -c n -f csv"
    instance_list_cmd =  cmd.run(instance_list.split(), check=True, capture_output=True)
    instance_qty = "wc -l"
    instance_qty_cmd = cmd.run(instance_qty.split(), input=instance_list_cmd.stdout, capture_output=True)
    instance_qty_cmd = instance_qty_cmd.stdout.decode('utf8').strip()
    return int(instance_qty_cmd)


@app.route('/')
def index():
    return render_template('lab.html', instances=return_instances(), instance_qty=return_instance_qty())

if __name__ == '__main__':
    app.run(port=25000)

from flask import Flask, render_template
import subprocess as cmd
import platform
import socket
import psutil
import logging
import json


app = Flask(__name__)


def return_system_info():
    try:
        info={}
        info['hostname']=socket.gethostname()
        info['platform']=platform.system()
        info['platform-release']=platform.release()
        info['platform-version']=platform.version()
        info['system temp (c)']=int(psutil.sensors_temperatures()['k10temp'][0][1])
        info['processor']=platform.processor()
        info['system ram']=f"{(round(psutil.virtual_memory().total / (1024.0 **3)))}GB"
        info['ram percent used']=f"{(round(psutil.virtual_memory()[2]))}%"
        info['ram used']=f"{(round(psutil.virtual_memory()[3]/1000000000))}GB"
        info['cpu cores']=int(psutil.cpu_count()/2)
        info['cpu utilization (last 5 seconds)']=f"{(psutil.cpu_percent(5))}%"
        info['5 minute Load Average']=round(psutil.getloadavg()[1],2)
        return info
    except Exception as e:
        logging.exception(e)


def return_instances():
    command = "lxc list -f json"
    instances = cmd.check_output(command.split(), shell=False)
    instances = instances.decode('utf8').replace("'", '"')
    lab_stack = json.loads(instances)
    return lab_stack


def return_instance_qty():
    instance_list = "lxc list -c n -f csv"
    instance_list_cmd =  cmd.run(instance_list.split(), check=True, capture_output=True)
    instance_qty = "wc -l"
    instance_qty_cmd = cmd.run(instance_qty.split(), input=instance_list_cmd.stdout, capture_output=True)
    instance_qty_cmd = instance_qty_cmd.stdout.decode('utf8').strip()
    return int(instance_qty_cmd)


def return_lxc_instance_qty():
    instance_list = "lxc list -c n,t,s -f csv"
    instance_list_cmd =  cmd.run(instance_list.split(), check=True, capture_output=True)
    instance_type = "grep -i container"
    instance_type_cmd = cmd.run(instance_type.split(), input=instance_list_cmd.stdout, capture_output=True)
    instance_qty = "wc -l"
    instance_qty_cmd = cmd.run(instance_qty.split(), input=instance_type_cmd.stdout, capture_output=True)
    instance_qty_cmd = instance_qty_cmd.stdout.decode('utf8').strip()
    return int(instance_qty_cmd)


def return_running_instance_qty():
    instance_list = "lxc list -c n,t,s -f csv"
    instance_list_cmd =  cmd.run(instance_list.split(), check=True, capture_output=True)
    instance_running = "grep -i running"
    instance_running_cmd = cmd.run(instance_running.split(), input=instance_list_cmd.stdout, capture_output=True)
    instance_qty = "wc -l"
    instance_qty_cmd = cmd.run(instance_qty.split(), input=instance_running_cmd.stdout, capture_output=True)
    instance_qty_cmd = instance_qty_cmd.stdout.decode('utf8').strip()
    return int(instance_qty_cmd)


def return_stopped_instance_qty():
    instance_list = "lxc list -c n,t,s -f csv"
    instance_list_cmd =  cmd.run(instance_list.split(), check=True, capture_output=True)
    instance_stopped = "grep -i stopped"
    instance_stopped_cmd = cmd.run(instance_stopped.split(), input=instance_list_cmd.stdout, capture_output=True)
    instance_qty = "wc -l"
    instance_qty_cmd = cmd.run(instance_qty.split(), input=instance_stopped_cmd.stdout, capture_output=True)
    instance_qty_cmd = instance_qty_cmd.stdout.decode('utf8').strip()
    return int(instance_qty_cmd)


@app.route('/')
def index():
    return render_template(
        'lab.html',
        instances=return_instances(),
        instance_qty=return_instance_qty(),
        lxc_instance_qty=return_lxc_instance_qty(),
        vm_instance_qty=return_instance_qty()-return_lxc_instance_qty(),
        running_instance_qty=return_running_instance_qty(),
        stopped_instance_qty=return_stopped_instance_qty(),
        system_info=return_system_info()
        )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=25000)

from flask import Flask, render_template
import subprocess as cmd
import platform
import socket
import psutil
import logging


app = Flask(__name__)


def return_system_info():
    try:
        info={}
        info['hostname']=socket.gethostname()
        info['platform']=platform.system()
        info['platform-release']=platform.release()
        info['platform-version']=platform.version()
        info['system temp (c)']=int(psutil.sensors_temperatures()['k10temp'][0][1])
        info['architecture']=platform.machine()
        info['processor']=platform.processor()
        info['system ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        print("DEBUG : type(info)")
        return info
    except Exception as e:
        logging.exception(e)


def return_instances():
    instance_list = []
    command = "lxc list -c n,limits.cpu:Cores,limits.memory:System-Ram,c,u,M,m,s,t,image.os:OS,user.comment:PROTECTED?,4 -f csv"
    instances = cmd.check_output(command.split(), shell=False)
    instances = instances.decode('utf8')
    instance_list = instances.split("\n")
    del instance_list[-1]
    return instance_list


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
    instance_type = "grep container"
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

from flask import Flask, render_template
import subprocess as cmd
import platform
import socket
import psutil
import logging
import json
import os
from datetime import timedelta


app = Flask(__name__)


def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
    sys_uptime = str(timedelta(seconds=uptime_seconds)).split(':')
    return(f"{sys_uptime[0]}:{sys_uptime[1]}:{sys_uptime[2]}")



def return_system_info():
    total_memory, used_memory, free_memory = map(
    int, os.popen('free -t -m').readlines()[-1].split()[1:])
    try:
        info={}
        info['Hostname']=socket.gethostname()
        info['Host OS Type']=platform.system()
        info['Kernel']=platform.release()
        info['Platform']=platform.version()
        try:
            info['System Temp (c)']=int(psutil.sensors_temperatures()['k10temp'][0][1])
        except KeyError:
            info['System Temp (c)']=0 #Tempory work around to set value to 0 if temp sensor not present on system, will put in long term fix in later commit
        info['Processor']=platform.processor()
        info['System RAM']=f"{round(total_memory)/1000}GB"
        info['RAM Utilization (%)']=f"{round((used_memory/total_memory) * 100, 2)}%"
        info['RAM Usage (GB)']=f"{round(used_memory)/1000}"
        info['cpu cores']=int(psutil.cpu_count()/2)
        info['cpu utilization (last 5 seconds)']=f"{(psutil.cpu_percent(5))}%"
        info['5 minute Load Average']=round(psutil.getloadavg()[1],2)
        info['15 minute Load Average']=round(psutil.getloadavg()[2],2)
        info['Host Uptime HH:MM:SS']=get_uptime()
        return info
    except Exception as e:
        logging.exception(e)


def return_instances():
    command = "lxc list -f json"
    instances = cmd.check_output(command.split(), shell=False)
    instances = instances.decode('utf8')
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


# @app.route('/')
# def index():
#     return render_template(
#         'notice.html',
#         )

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

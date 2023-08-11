import platform
import socket
import re
import uuid
import psutil
import logging


def return_system_info():
    try:
        info={}
        info['platform']=platform.system()
        info['platform-release']=platform.release()
        info['platform-version']=platform.version()
        info['architecture']=platform.machine()
        info['hostname']=socket.gethostname()
        info['ip-address']=socket.gethostbyname(socket.gethostname())
        try:
            info['system temp (c)']=int(psutil.sensors_temperatures()['k10temp'][0][1])
        except KeyError:
            next
        info['mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor']=platform.processor()
        info['ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        print(f"DEBUG : {type(info)}")
        return info
    except Exception as e:
        logging.exception(e)



if __name__ == '__main__':
    print(return_system_info())

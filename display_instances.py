import subprocess as cmd
import json


def return_instances():
    command = "lxc list -f json"
    instances = cmd.check_output(command.split(), shell=False)
    instances = instances.decode('utf8').replace("'", '"')
    data = json.loads(instances)
    return data


def return_instance_qty():
    instance_list = "lxc list -c n -f csv"
    instance_list_cmd =  cmd.run(instance_list.split(), check=True, capture_output=True)
    instance_qty = "wc -l"
    instance_qty_cmd = cmd.run(instance_qty.split(), input=instance_list_cmd.stdout, capture_output=True)
    instance_qty_cmd = instance_qty_cmd.stdout.decode('utf8').strip()
    return int(instance_qty_cmd)


def return_lxc_instance_qty():
    instance_list = "lxc list -c n -f csv"
    instance_list_cmd =  cmd.run(instance_list.split(), check=True, capture_output=True)
    instance_type = "grep container"
    instance_type_cmd = cmd.run(instance_type.split(), input=instance_list_cmd.stdout, capture_output=True)
    instance_qty = "wc -l"
    instance_qty_cmd = cmd.run(instance_qty.split(), input=instance_type_cmd.stdout, capture_output=True)
    instance_qty_cmd = instance_qty_cmd.stdout.decode('utf8').strip()
    return int(instance_qty_cmd)


def return_running_instance_qty():
    instance_list = "lxc list -c n -f csv"
    instance_list_cmd =  cmd.run(instance_list.split(), check=True, capture_output=True)
    instance_running = "grep -i running"
    instance_running_cmd = cmd.run(instance_running.split(), input=instance_list_cmd.stdout, capture_output=True)
    instance_qty = "wc -l"
    instance_qty_cmd = cmd.run(instance_qty.split(), input=instance_running_cmd.stdout, capture_output=True)
    instance_qty_cmd = instance_qty_cmd.stdout.decode('utf8').strip()
    return int(instance_qty_cmd)


def main():
    cmd.call("clear", shell=False)
    print(f"Running Instances Qty : {return_instance_qty()}")
    print(f"LXC Container Instances Qty  : {return_lxc_instance_qty()}")
    print(f"QEMU VM Instances Qty : {return_instance_qty() - return_lxc_instance_qty()}")
    print(f"Running Instances Qty : {return_running_instance_qty()}")
    print(f"Running Instances Info : {return_instances()}")
    print(f"Running Instances Info Type : {type(return_instances())}")


if __name__ == '__main__':
    main()

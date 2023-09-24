import ipdb

# Following tutorial at https://www.w3schools.com/python/python_classes.asp

# Create Instance Parent Class with properties for type, name, ram and cpu
class MyInstance:
    def __init__(self,type, name, ram, cpu):
        self.type = type # VM or Container
        self.name = name
        self.ram = ram # Allocated as Integer in GB
        self.cpu = cpu # Cores allocated

    # print user friendly string if printing the object directly
    def __str__(self):
        return f"{self.name}({self.type})"

    # Object method example
    def returnRamInMb(self):
        return f"RAM {self.ram * 1024}MB"


# Create an Object from the Class declared above
vm = MyInstance("vm", "ubuntu", 4, 4)

print(f"Object : {vm} and its type is : {type(vm)}")
print(f"Name : {vm.name}")
print(f"Type : {vm.type}")
print(f"RAM : {vm.returnRamInMb()}")
print(f"Will rename instance from {vm.name} to 'debian'")
vm.name = "debian"
print(f"New Name : {vm.name}")

# Create child Class to inherit instance class for Linux Instances
# Following inheritance is broken needs to be fixed :(
class Linux(MyInstance):
    def __init__(self,type, name, ram, cpu, os_type):
        super().__init__(self, type, name, ram)
        self.os_type = os_type

container = Linux("vm", "debian", 6, 4, "linux")

ipdb.set_trace()

print(f"Object : {container} and its type is : {type(container)}")
print(f"Name : {container.name}")
print(f"Type : {container.type}")
print(f"RAM : {container.returnRamInMb()}")
print(f"Will rename instance from {container.name} to 'debian'")
container.name = "alpine"
print(f"New Name : {container.name}")

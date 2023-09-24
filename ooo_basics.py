# Following tutorial at https://www.w3schools.com/python/python_classes.asp

class MyInstance:
    def __init__(self,type, name, ram, cpu):
        self.type = type # VM or Container
        self.name = name
        self.ram = ram # Allocated as Integer in GB
        self.cpu = cpu # Cores allocated


    def __str__(self):
        return f"{self.name}({self.type})"


    def returnRamInMb(self):
        return f"RAM {self.ram * 1024}MB"


vm = MyInstance("vm", "ubuntu", 4, 4)

print(vm)
print(type(vm))
print(vm.name)
print(vm.type)
print(vm.returnRamInMb())

import abc

class Thing(abc.ABC):
    @abc.abstractmethod
    def __init__(self, name):
        self.name = name
        print(f"Create thing {self.name}")

    @abc.abstractmethod
    def print_name(self):
        print(f'name this device is {self.name}')

class Sensor(Thing):
    def __init__(self, name):
        super().__init__(name)
        self.value = 20

    def print_name(self):
        super().print_name()

class Device(Thing):
    def __init__(self, name, setValue):
        super().__init__(name)
        self.value_const = setValue

    def print_name(self):
        super().print_name()

class SensorSim(Sensor):
    def valueUp(self, *sensors):
        for sensor in sensors:
            sensor.value += 1
            print(f"Change value up of sensor: {self.name}, on {sensor.value}")
    def valueDown(self, *sensors):
        for sensor in sensors:
            sensor.value -= 1
            print(f"Change value down of sensor: {self.name}, on {sensor.value}")
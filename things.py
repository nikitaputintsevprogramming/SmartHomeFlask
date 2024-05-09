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
        print(f"Create new device {self.name}")

    def print_name(self):
        super().print_name()


class Humidifier(Thing):
    def __init__(self, name, focus_wet):
        super().__init__(name)
        self.focus_wet = focus_wet

    def print_name(self):
        super().print_name()

    def humidify(self, *sensors):
        for sensor in sensors:
            if sensor.value < self.focus_wet:
                sensor.value += 1
            else:
                sensor.value -= 1
class Vehicle:
    def __init__(self, speed):
        self.speed = speed

    def start_engine(self):
        print("Engine started.")

class Electric:
    def __init__(self, battery_level):
        self.battery_level = battery_level

    def charge(self):
        print(f"Charging... Battery at {self.battery_level}%")

class ElectricCar(Vehicle, Electric):
    def __init__(self, speed, battery_level):
        Vehicle.__init__(self, speed)
        Electric.__init__(self, battery_level)

# Demonstrate usage
ecar = ElectricCar(120, 85)
ecar.start_engine()   # From Vehicle
ecar.charge()         # From Electric

# Method Resolution Order (MRO)
print("MRO:", [cls.__name__ for cls in ElectricCar.__mro__])

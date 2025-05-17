class Temperature:
    def __init__(self, celsius):
        self._celsius = None
        self.celsius = celsius  # Uses the setter for validation

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature cannot be below absolute zero!")
        self._celsius = value

    def get_fahrenheit(self):
        return (self._celsius * 9/5) + 32

# Example usage
temp = Temperature(25)
print("Celsius:", temp.celsius)
print("Fahrenheit:", temp.get_fahrenheit())

temp.celsius = 100
print("Updated Celsius:", temp.celsius)
print("Updated Fahrenheit:", temp.get_fahrenheit())

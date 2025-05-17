import math

class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius

# Create a Circle object and print area and perimeter
circle = Circle(5)
print("Area:", circle.area())
print("Perimeter:", circle.perimeter())

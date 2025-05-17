from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height

def print_area(shape: Shape):
    print("Area:", shape.area())

# Create instances and demonstrate polymorphism
rect = Rectangle(4, 5)
tri = Triangle(6, 3)

print_area(rect)
print_area(tri)

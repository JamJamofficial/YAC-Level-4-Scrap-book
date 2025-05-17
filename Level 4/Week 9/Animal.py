class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print("The animal makes a sound.")

class Cat(Animal):
    def speak(self):
        print(f"{self.name} says: Meow!")

class Bird(Animal):
    def speak(self):
        print(f"{self.name} says: Chirp!")

# Create instances and call speak
cat = Cat("Whiskers")
bird = Bird("Tweety")

cat.speak()
bird.speak()

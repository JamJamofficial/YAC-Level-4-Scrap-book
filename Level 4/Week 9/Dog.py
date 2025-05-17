class Dog:
    def __init__(self, name, breed, age):
        self.name = name
        self.breed = breed
        self.age = age

    def bark(self):
        print(f"{self.name} says: Woof!")

# Create Dog objects and call bark
dog1 = Dog("Buddy", "Golden Retriever", 3)
dog2 = Dog("Luna", "Beagle", 2)

dog1.bark()
dog2.bark()

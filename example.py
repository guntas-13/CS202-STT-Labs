class Animal:
    """Docstring for Animal class.

    Args:
        object (object): Base class for all classes in Python.
    """
    def __init__(self, name):
        self.name = name

    def eat(self, food):
        """Docstring for eat method.

        Args:
            food (str): Food to eat.
        """
        print(f"{self.name} eats {food}")


class Dog(Animal):
    """Docstring for Dog class.

    Args:
        Animal (object): Base class for all classes in Python.
    """
    def fetch(self, thing):
        """Docstring for fetch method.

        Args:
            thing (str): Thing to fetch.
        """
        print(f"{self.name} goes after the {thing}!")

    def show_affection(self):
        """Docstring for show_affection method.
        """
        print(f"{self.name} wags tail")


class Cat(Animal):
    """Docstring for Cat class.

    Args:
        Animal (object): Base class for all classes in Python.
    """
    def swatstring(self):
        """Docstring for swatstring method.
        """
        print(f"{self.name} shreds more string")

    def show_affection(self):
        """Docstring for show_affection method.
        """
        print(f"{self.name} purrs")


for a in (Dog("Rover"), Cat("Fluffy"), Cat("Lucky"), Dog("Scout")):
    a.show_affection()

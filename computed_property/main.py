from math import sqrt
from computed_property import computed_property

# Teste com a classe Vector
class Vector:
    def __init__(self, x, y, z, color=None):
        self.x, self.y, self.z = x, y, z
        self.color = color

    @computed_property('x', 'y', 'z')
    def magnitude(self):
        """Magnitude of the vector"""
        print('computing magnitude')
        return sqrt(self.x**2 + self.y**2 + self.z**2)

v = Vector(9, 2, 6)
print(v.magnitude)  # computing magnitude -> 11.0
v.color = 'red'
print(v.magnitude)  # 11.0
v.y = 18
print(v.magnitude)  # computing magnitude -> 21.0

# Teste com Circle e métodos setter/deleter
class Circle:
    def __init__(self, radius=1):
        self.radius = radius

    @computed_property('radius')
    def diameter(self):
        """Circle diameter from radius"""
        print('computing diameter')
        return self.radius * 2

    @diameter.setter
    def diameter(self, diameter):
        self.radius = diameter / 2

    @diameter.deleter
    def diameter(self):
        self.radius = 0

circle = Circle()
print(circle.diameter)  # computing diameter -> 2
circle.diameter = 3
print(circle.radius)  # 1.5
del circle.diameter
print(circle.radius)  # 0

# Testando docstrings
help(computed_property)

import math


class Length(object):
    pass


class Inch(Length):
    def __init__(self, inches: int):
        self.inches = inches
        pass


class Foot(Length):
    def __init__(self, feet: int, inches=0):
        self.inches = inches % 12
        self.feet = feet + math.trunc(inches/12)

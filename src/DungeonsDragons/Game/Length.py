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
        pass

class Yard(Length):
    def __init__(self, yards: int, feet=0, inches=0):
        self.inches = inches % 12
        self.feet = (feet + math.trunc(inches/12)) % 3
        self.yards = yards + math.trunc((feet + math.trunc(inches/12))/3)
        pass

class Mile(Length):
    def __init__(self, miles: int, yards=0, feet=0, inches=0):
        self.inches = inches % 12
        self.feet = (feet + math.trunc(inches/12)) % 3
        self.yards = yards + math.trunc((feet + math.trunc(inches/12))/3) % 1760
        self.miles = miles + math.trunc((yards + math.trunc((feet + math.trunc(inches/12))/3))/1760)
        pass

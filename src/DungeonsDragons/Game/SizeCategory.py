from enum import Enum


class SizeCategory(Enum):
    Tiny = (2.5)
    Small = (5)
    Medium = (5)
    Large = (10)
    Huge = (15)
    Gargantuan = (20)

    def __init__(self, dimension):
        self.dimension = dimension

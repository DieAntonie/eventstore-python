from enum import Enum


class SizeCategory(Enum):
    Tiny = "xs"
    Small = "s"
    Medium = "m"
    Large = "l"
    Huge = "xl"
    Gargantuan = "xxl"

    def __init__(self, dimension):
        self.dimension = dimension

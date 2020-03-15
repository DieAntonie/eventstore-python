from enum import Enum


class Dice(Enum):
    FourSidedDie = "d4"
    SixSidedDie = "d6"
    EightSidedDie = "d8"
    TenSidedDie = "d10"
    TwelveSidedDie = "d12"
    TwentySidedDie = "d20"
    PercentileDice = "d100"


class DiceRoll():
    def __init__(self, times: int, dice: Dice):
        self.times = times
        self.dice = dice
from enum import Enum


class Ability(Enum):
    Strength = "str"
    Dexterity = "dex"
    Constitution = "con"
    Intelligence = "int"
    Wisdom = "wis"
    Charisma = "cha"
    Any = "*"
    Other = "!"

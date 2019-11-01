from enum import Enum
from .Language import Language
from .SizeCategory import SizeCategory
from .Ability import Ability
from .DamageType import DamageType
from .AreaOfEffect import (
    AreaOfEffect,
    Cone,
    Line
)


class Race(Enum):
    pass


class Dragonborn(Race):
    Black = (DamageType.Acid, Line(5, 30), Ability.Dexterity)
    Blue = (DamageType.Lightning, Line(5, 30), Ability.Dexterity)
    Brass = (DamageType.Fire, Line(5, 30), Ability.Dexterity)
    Bronze = (DamageType.Lightning, Line(5, 30), Ability.Dexterity)
    Copper = (DamageType.Acid, Line(5, 30), Ability.Dexterity)
    Gold = (DamageType.Fire, Cone(30), Ability.Dexterity)
    Green = (DamageType.Poison, Cone(30), Ability.Constitution)
    Red = (DamageType.Fire, Cone(30), Ability.Dexterity)
    Silver = (DamageType.Cold, Cone(30), Ability.Constitution)
    White = (DamageType.Cold, Cone(30), Ability.Constitution)

    def __init__(self, damage_type: DamageType, area_of_effect: AreaOfEffect, saving_throw: Ability):
        # Subrace trait variations
        self.damage_type = damage_type
        self.area_of_effect = area_of_effect
        self.saving_throw = saving_throw

        # Parent race traits
        self.speed = 30
        self.size = SizeCategory.Medium
        self.language = [Language.Draconic]
        self.ability_score_modifier = {
            Ability.Strength: 2,
            Ability.Charisma: 1
        }


class Dwarf(Race):
    pass


class Elf(Race):
    pass


class Halfelf(Race):
    pass


class Halfling(Race):
    pass


class Halforc(Race):
    pass


class Human(Race):
    pass


class Tiefling(Race):
    pass


class Aasimar(Race):
    pass


class Bugbear(Race):
    pass


class Firbolg(Race):
    pass


class Goblin(Race):
    pass


class Hobgoblin(Race):
    pass


class Kenku(Race):
    pass


class Kobold(Race):
    pass


class Lizardfolk(Race):
    pass


class Orc(Race):
    pass


class Tabaxi(Race):
    pass


class Triton(Race):
    pass


class Yuanti(Race):
    pass

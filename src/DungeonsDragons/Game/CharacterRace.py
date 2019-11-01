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


class CharacterRace(Enum):
    pass


class Dragonborn(CharacterRace):
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


class Dwarf(CharacterRace):
    pass


class Elf(CharacterRace):
    pass


class Halfelf(CharacterRace):
    pass


class Halfling(CharacterRace):
    pass


class Halforc(CharacterRace):
    pass


class Human(CharacterRace):
    pass


class Tiefling(CharacterRace):
    pass


class Aasimar(CharacterRace):
    pass


class Bugbear(CharacterRace):
    pass


class Firbolg(CharacterRace):
    pass


class Goblin(CharacterRace):
    pass


class Hobgoblin(CharacterRace):
    pass


class Kenku(CharacterRace):
    pass


class Kobold(CharacterRace):
    pass


class Lizardfolk(CharacterRace):
    pass


class Orc(CharacterRace):
    pass


class Tabaxi(CharacterRace):
    pass


class Triton(CharacterRace):
    pass


class Yuanti(CharacterRace):
    pass

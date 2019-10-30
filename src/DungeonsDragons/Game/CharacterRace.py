from enum import Enum


class Script(Enum):
    Celestial = 1
    Common = 2
    Draconic = 3
    Dwarvish = 4
    Elvish = 5
    Infernal = 6


class Language(Enum):
    Common = (Script.Common)
    Dwarvish = (Script.Dwarvish)
    Elvish = (Script.Elvish)
    Giant = (Script.Dwarvish)
    Gnomish = (Script.Dwarvish)
    Goblin = (Script.Dwarvish)
    Halfling = (Script.Common)
    Orc = (Script.Dwarvish)
    Abyssal = (Script.Infernal)
    Celestial = (Script.Celestial)
    Draconic = (Script.Draconic)
    DeepSpeech = (None)
    Infernal = (Script.Infernal)
    Primordial = (Script.Dwarvish)
    Sylvan = (Script.Elvish)
    Undercommon = (Script.Elvish)

    def __init__(self, script: Script):
        self.script = script


class Alignment(Enum):
    LawfulGood = "LG"
    NeutralGood = "NG"
    ChaoticGood = "CG"
    LawfulNeutral = "LN"
    Neutral = "N"
    ChaoticNeutral = "CN"
    LawfulEvil = "LE"
    NeutralEvil = "NE"
    ChaoticEvil = "CE"


class SizeCategory(Enum):
    Tiny = (2.5)
    Small = (5)
    Medium = (5)
    Large = (10)
    Huge = (15)
    Gargantuan = (20)

    def __init__(self, dimension):
        self.dimension = dimension


class Ability(Enum):
    Strength = "str"
    Dexterity = "dex"
    Constitution = "con"
    Intelligence = "int"
    Wisdom = "wis"
    Charisma = "cha"


class DamageType(Enum):
    Acid = 1
    Bludgeoning = 2
    Cold = 3
    Fire = 4
    Force = 5
    Lightning = 6
    Necrotic = 7
    Piercing = 8
    Poison = 9
    Psychic = 10
    Radiant = 12
    Slashing = 13
    Thunder = 14


class AreaOfEffect(object):
    pass


class Line(AreaOfEffect):
    def __init__(self, width, length):
        pass


class Cone(AreaOfEffect):
    def __init__(self, length):
        pass


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

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

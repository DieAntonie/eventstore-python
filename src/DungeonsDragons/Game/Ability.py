from enum import Enum
from typing import Sequence


class Ability(Enum):
    Strength = "str"
    Dexterity = "dex"
    Constitution = "con"
    Intelligence = "int"
    Wisdom = "wis"
    Charisma = "cha"
    Any = "*"
    Other = "!"


class AbilityScore(object):
    def __init__(self, ability: Ability, score: int):
        self.ability = ability
        self.score = score


class AbilityScoreIncrease(object):
    def __init__(self, *ability_scores: Sequence[AbilityScore]):
        self.abilities = {
            Ability.Strength: 0,
            Ability.Dexterity: 0,
            Ability.Constitution: 0,
            Ability.Intelligence: 0,
            Ability.Wisdom: 0,
            Ability.Charisma: 0
        }
        self.any = []
        self.other = []

        for ability_score in ability_scores:
            if ability_score.ability in self.abilities:
                self.abilities[ability_score.ability] += ability_score.score
            elif ability_score.ability is Ability.Any:
                self.any.append(ability_score.score)
            elif ability_score.ability is Ability.Other:
                self.other.append(ability_score.score)
            self._validate_integrity()

    def _validate_integrity(self):
        if len(self.other) >= len([ability for ability, score in self.abilities.items() if score == 0]):
            raise Exception("Too Many `Other` Ability Score Increases")

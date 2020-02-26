class RaceAlreadyCreated(Exception):
    """
    Requested command denied because `Race` is already set on `CharacterAggregate`.
    """
    pass


class RaceCannotBeBasedOnSelf(Exception):
    """
    Requested command denied because `Race` is already set on `CharacterAggregate`.
    """
    pass


class RaceDoesNotExist(Exception):
    """
    Requested command denied because `Race` is already set on `CharacterAggregate`.
    """
    pass


class TooManyOtherAbilityScoreIncreaseTokens(Exception):
    """
    Deny invalid command because there are more or an equal amount of `Other` tokens for available `Ability` options.  
    """
    pass


class InvalidAbilityScoreIncreaseTokenStructure(Exception):
    """
    Deny invalid command because of the token structure has invalid amount of `Ability` modifiers.  
    """
    pass


class InvalidAbilityScoreIncreaseToken(Exception):
    """
    Deny invalid command because of unrecognized token used.  
    """
    pass


class RaceMaturityAgeExceedsLifeExpectency(Exception):
    """
    Deny invalid command because maturity age exceeds life expectency.  
    """
    pass


class RaceMaturityAgeTooSmall(Exception):
    """
    Deny invalid command because maturity age is too small.  
    """
    pass


class CharacterRaceAlreadyCreated(Exception):
    """
    Requested command denied because `Race` is already set on `CharacterAggregate`.
    """
    pass


class CharacterRaceNameDoesNotDiffer(Exception):
    """
    Requested command denied because `Race` is already set on `CharacterAggregate`.
    """
    pass

class CharacterRaceDoesNotExist(Exception):
    """
    Requested command denied because `Race` is already set on `CharacterAggregate`.
    """
    pass

class CharacterSubraceNameDoesNotDifferFromBaseRace(Exception):
    """
    Requested command denied because `Race` is already set on `CharacterAggregate`.
    """
    pass

class CharacterSubraceAlreadyExists(Exception):
    """
    Requested command denied because `Race` is already set on `CharacterAggregate`.
    """
    pass

class CharacterSubraceDoesNotExists(Exception):
    pass
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

class RaceNameDoesNotDiffer(Exception):
    """
    Requested command denied because `Race` is already set on `CharacterAggregate`.
    """
    pass

class RaceDoesNotExist(Exception):
    """
    Requested command denied because `Race` is already set on `CharacterAggregate`.
    """
    pass

class subraceNameDoesNotDifferFromBaseRace(Exception):
    """
    Requested command denied because `Race` is already set on `CharacterAggregate`.
    """
    pass

class subraceAlreadyExists(Exception):
    """
    Requested command denied because `Race` is already set on `CharacterAggregate`.
    """
    pass

class subraceDoesNotExists(Exception):
    pass
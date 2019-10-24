class TabNotOpen(Exception):
    """
    Requested command denied because `TabAggregate` is not open.
    """
    pass


class DrinksNotOutstanding(Exception):
    """
    Requested command denied because `TabAggregate` does not have some drink outstanding.
    """
    pass


class FoodNotOutstanding(Exception):
    """
    Requested command denied because `TabAggregate` does not have some food outstanding.
    """
    pass


class FoodNotPrepared(Exception):
    """
    Requested command denied because `TabAggregate` does not have some food prepared.
    """
    pass


class MustPayEnough(Exception):
    """
    Requested command denied because amount paid for `TabAggregate` must be greater than served items value.
    """
    pass


class TabHasUnservedItems(Exception):
    """
    Requested command denied because `TabAggregate` has some outstanding drinks and food or unprepared food.
    """
    pass

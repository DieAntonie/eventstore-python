from functools import singledispatch, update_wrapper
from ...Infrastructure.Aggregate import Aggregate


class EnvironmentAggregate(Aggregate):
    """
    An instance of the Tab domain object.
    """

    def __init__(self):
        super().__init__()

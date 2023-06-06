from functools import singledispatch, update_wrapper
from ...Infrastructure.IAggregate import IAggregate


class EnvironmentAggregate(IAggregate):
    """
    An instance of the Tab domain object.
    """

    def __init__(self):
        super().__init__()

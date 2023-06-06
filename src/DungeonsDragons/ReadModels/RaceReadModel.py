from dataclasses import dataclass
import threading
from typing import Optional
import uuid
from ...Infrastructure.IReadModel import IReadModel
from ..Game.Race.Events import (
    RaceCreated,
    RaceNameSet
)

class RaceReadModel(IReadModel):

    @dataclass
    class Race():
        Id: uuid.UUID
        Name : Optional[str] = None
        
    def __init__(self) -> None:
        self.races = {}
        self.lock = threading.Lock()

    def ActiveRaces(self) -> list[Race]:
        self.lock.acquire()
        try:
            return [self.races[race_id] for race_id in self.races]
        finally:
            self.lock.release()
    
    @IReadModel.Handle.register(RaceCreated)
    def Handle_RaceCreated(self, event: RaceCreated):
        """
        `RaceSet` event handler that opens this `TabAggregate`.
        """
        self.lock.acquire()
        try:
            self.races[event.Id] = self.Race(event.Id)
        finally:
            self.lock.release() 

    @IReadModel.Handle.register(RaceNameSet)
    def Handle_RaceNameSet(self, event: RaceNameSet):
        """
        `RaceSet` event handler that opens this `TabAggregate`.
        """
        self.lock.acquire()
        try:
            self.races[event.Id].Name = event.Name
        finally:
            self.lock.release() 
        
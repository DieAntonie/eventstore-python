import threading
from ...Infrastructure.IReadModel import IReadModel
from ..Game.Race.Events import RaceAbilityScoreIncreaseSet, RaceBaseHeightSet, RaceBaseWalkSpeedSet, RaceBaseWeightSet, RaceCreated, RaceDescriptionSet, RaceHeightModifierSet, RaceLanguagesSet, RaceLifeExpectancySet, RaceMaturityAgeSet, RaceMoralitySet, RaceNameSet, RaceOrthodoxySet, RaceSizeCategorySet, RaceSubRacesSet, RaceWeightModifierSet

class RaceReadModel(IReadModel):
    def __init__(self) -> None:
        self.races = {}
        self.lock = threading.Lock()

    
    @IReadModel.Handle.register(RaceCreated)
    def Handle_RaceCreated(self, event: RaceCreated):
        """
        `RaceSet` event handler that opens this `TabAggregate`.
        """
        self.Id = event.Id
        self.base_race = event.BaseRaceId

    @IReadModel.Handle.register(RaceNameSet)
    def Handle_RaceNameSet(self, event: RaceNameSet):
        """
        `RaceSet` event handler that opens this `TabAggregate`.
        """
        self.name = event.Name

    @IReadModel.Handle.register(RaceDescriptionSet)
    def Handle_RaceDescriptionSet(self, event: RaceDescriptionSet):
        """
        `RaceSet` event handler that opens this `TabAggregate`.
        """
        self.description = event.Description

    @IReadModel.Handle.register(RaceAbilityScoreIncreaseSet)
    def Handle_RaceAbilityScoreIncreaseSet(self, event: RaceAbilityScoreIncreaseSet):
        """
        `RaceSet` event handler that opens this `TabAggregate`.
        """
        self.ability_score_increase = event.AbilityScoreIncrease

    @IReadModel.Handle.register(RaceMaturityAgeSet)
    def Handle_RaceMaturityAgeSet(self, event: RaceMaturityAgeSet):
        """
        `RaceMaturityAgeSet` event handler that sets this `RaceAggregate.maturity_age`.
        """
        self.maturity_age = event.MaturityAge

    @IReadModel.Handle.register(RaceLifeExpectancySet)
    def Handle_RaceLifeExpectancySet(self, event: RaceLifeExpectancySet):
        """
        `RaceLifeExpectancySet` event handler that sets this `RaceAggregate.life_expectency`.
        """
        self.life_expectency = event.LifeExpectency

    @IReadModel.Handle.register(RaceOrthodoxySet)
    def Handle_RaceOrthodoxySet(self, event: RaceOrthodoxySet):
        """
        `RaceOrthodoxySet` event handler that sets this `RaceAggregate.orthodoxy`.
        """
        self.orthodoxy = event.Orthodoxy

    @IReadModel.Handle.register(RaceMoralitySet)
    def Handle_RaceMoralitySet(self, event: RaceMoralitySet):
        """
        `RaceMoralitySet` event handler that sets this `RaceAggregate.morality`.
        """
        self.morality = event.Morality

    @IReadModel.Handle.register(RaceSizeCategorySet)
    def Handle_RaceSizeCategorySet(self, event: RaceSizeCategorySet):
        """
        `RaceSizeCategorySet` event handler that sets this `RaceAggregate.size_category`.
        """
        self.size_category = event.SizeCategory

    @IReadModel.Handle.register(RaceBaseHeightSet)
    def Handle_RaceBaseHeightSet(self, event: RaceBaseHeightSet):
        """
        `RaceBaseHeightSet` event handler that sets this `RaceAggregate.base_height`.
        """
        self.base_height = event.BaseHeight

    @IReadModel.Handle.register(RaceHeightModifierSet)
    def Handle_RaceHeightModifierSet(self, event: RaceHeightModifierSet):
        """
        `RaceHeightModifierSet` event handler that sets this `RaceAggregate.height_modifier`.
        """
        self.height_modifier = event.HeightModifier

    @IReadModel.Handle.register(RaceBaseWeightSet)
    def Handle_RaceBaseWeightSet(self, event: RaceBaseWeightSet):
        """
        `RaceBaseWeightSet` event handler that sets this `RaceAggregate.base_weight`.
        """
        self.base_weight = event.BaseWeight

    @IReadModel.Handle.register(RaceWeightModifierSet)
    def Handle_RaceWeightModifierSet(self, event: RaceWeightModifierSet):
        """
        `RaceWeightModifierSet` event handler that sets this `RaceAggregate.weight_modifier`.
        """
        self.weight_modifier = event.WeightModifier

    @IReadModel.Handle.register(RaceBaseWalkSpeedSet)
    def Handle_RaceBaseWalkSpeedSet(self, event: RaceBaseWalkSpeedSet):
        """
        `RaceBaseWalkSpeedSet` event handler that sets this `RaceAggregate.base_walk_speed`.
        """
        self.base_walk_speed = event.BaseWalkSpeed

    @IReadModel.Handle.register(RaceLanguagesSet)
    def Handle_RaceLanguagesSet(self, event: RaceLanguagesSet):
        """
        `RaceLanguagesSet` event handler that sets this `RaceAggregate.base_walk_speed`.
        """
        self.languages = event.Languages

    @IReadModel.Handle.register(RaceSubRacesSet)
    def Handle_RaceLanguagesSet(self, event: RaceSubRacesSet):
        """
        `RaceSubRacesSet` event handler that sets this `RaceAggregate.base_walk_speed`.
        """
        self.sub_races = event.Subraces
        
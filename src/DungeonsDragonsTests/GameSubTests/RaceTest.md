# Race Test

A suite of tests verifies the behavioural functionality of the [`RaceAggregate`](../../DungeonsDragons/Game/Race/Race.md)

## Index
1. [Setup](#setup)
2. [Race Creation](#race-creation)
3. [Race Details](#race-details)
4. [Race Ability Score Increase](#race-ability-score-increase)
5. [Race Age](#race-age)
6. [Race Alignment](#race-alignment)
6. [Race Size](#race-size)

## Setup
### The set of values used in determining whether expected outcomes are achieved.

Alias                                           |   Value                                                           |
------------------------------------------------|-------------------------------------------------------------------|
**`RaceId`**                                    | '_uuid.UUID_'                                                     |
**`SubraceId`**                                 | '_uuid.UUID_'                                                     |
**`RaceName1`**                                 | '_Race 1_'                                                        |
**`RaceName2`**                                 | '_Race 2_'                                                        |
**`RaceDescription1`**                          | '_Description 1_'                                                 |
**`RaceDescription2`**                          | '_Description 2_'                                                 |
**`ValidAbilityScoreIncrease`**                 | '_[{`str`:2}, {`int`:1}, {`*`:1}, {`!`:1}]_'                      |
**`InvalidAbilityScoreIncrease`**               | '_[{`str`:2}, {`int`:1}, {`con`:1}, {`!`:1}, {`!`:1}, {`!`:1}]_'  |
**`InvalidAbilityScoreIncreaseTokenStructure`** | '_[{`str`:2, `int`:1}]_'                                          |
**`InvalidAbilityScoreIncreaseToken`**          | '_[{`value`:2}]_'                                                 |
**`MaturityAge1`**                              | '_19_'                                                            |
**`MaturityAge2`**                              | '_75_'                                                            |
**`LifeExpectencyAge1`**                        | '_100_'                                                           |
**`LifeExpectencyAge2`**                        | '_50_'                                                            |
**`ZeroAge`**                                   | '_0_'                                                             |
**`Lawful`**                                    | '_1_'                                                             |
**`Good`**                                      | '_1_'                                                             |
**`Chaotic`**                                   | '_-1_'                                                            |
**`Evil`**                                      | '_-1_'                                                            |
**`OverlyLawful`**                              | '_1.1_'                                                           |
**`OverlyGood`**                                | '_1.1_'                                                           |
**`OverlyChaotic`**                             | '_-1.1_'                                                          |
**`OverlyEvil`**                                | '_-1.1_'                                                          |
**`MediumSize`**                                | '_SizeCategory.Medium_'                                           |
**`FourFootEight`**                             | '_4' 8"_'                                                         |
**`TwoTenSidedDie`**                            | '_2d10_'                                                          |
**`HundredAndTenPounds`**                       | '_110 lb_'                                                        |
**`ThreeFourSidedDie`**                         | '_3d4_'                                                           |

## Race Creation
### Can create Race
1. Given event(s):
    - None
2. When command:
    - `CreateRace` is issued with
        - `Id = RaceId`
        - `BaseRaceId = None`
3. Then expect event(s):
    - `RaceCreated` with
        - `Id = RaceId`
        - `BaseRaceId = None`

### Cannot create same Race more than once
1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
2. When command:
    - `CreateRace` is issued with
        - `Id = RaceId`
        - `BaseRaceId = None`
3. Then expect exception:
    - `RaceAlreadyCreated`

### Can create Race based on other
1. Given event(s):
    - None
2. When command:
    - `CreateRace` is issued with
        - `Id = SubraceId`
        - `BaseRaceId = RaceId`
3. Then expect event(s):
    - `RaceCreated` with
        - `Id = SubraceId`
        - `BaseRaceId = RaceId`

### Cannot create Race based on itself
1. Given event(s):
    - None
2. When command:
    - `CreateRace` is issued with
        - `Id = RaceId`
        - `BaseRaceId = RaceId`
3. Then expect exception:
    - `RaceCannotBeBasedOnSelf`

## Race Details
### Can set Race details
1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
2. When command:
    - `SetRaceDetails` is issued with
        - `Id = RaceId`
        - `Name = RaceName1`
        - `Description = RaceDescription1`
3. Then expect event(s):
    - `RaceNameSet` with
        - `Id = RaceId`
        - `Name = RaceName1`
    - `RaceDescriptionSet` with
        - `Id = RaceId`
        - `Description = RaceDescription1`

### Can set Race details unchanged
1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
    - `RaceNameSet` with
        - `Id = RaceId`
        - `Name = RaceName1`
    - `RaceDescriptionSet` with
        - `Id = RaceId`
        - `Description = RaceDescription1`
2. When command:
    - `SetRaceDetails` is issued with
        - `Id = RaceId`
        - `Name = RaceName1`
        - `Description = RaceDescription1`
3. Then expect event(s):
    - None

### Can set Race details with same name
1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
    - `RaceNameSet` with
        - `Id = RaceId`
        - `Name = RaceName1`
    - `RaceDescriptionSet` with
        - `Id = RaceId`
        - `Description = RaceDescription1`
2. When command:
    - `SetRaceDetails` is issued with
        - `Id = RaceId`
        - `Name = RaceName1`
        - `Description = RaceDescription2`
3. Then expect event(s):
    - `RaceDescriptionSet` with
        - `Id = RaceId`
        - `Description = RaceDescription2`

### Can set Race details with same description
1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
    - `RaceNameSet` with
        - `Id = RaceId`
        - `Name = RaceName1`
    - `RaceDescriptionSet` with
        - `Id = RaceId`
        - `Description = RaceDescription1`
2. When command:
    - `SetRaceDetails` is issued with
        - `Id = RaceId`
        - `Name = RaceName2`
        - `Description = RaceDescription1`
3. Then expect event(s):
    - `RaceNameSet` with
        - `Id = RaceId`
        - `Name = RaceName2`

### Cannot set uncreated Race details
1. Given event(s):
    - None
2. When command:
    - `SetRaceDetails` is issued with
        - `Id = RaceId`
        - `Name = RaceName1`
        - `Description = RaceDescription1`
3. Then expect exception:
    - `RaceDoesNotExist`

## Race Ability Score Increase
### Can set Race ability score increase
1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
2. When command:
    - `SetRaceAbilityScoreIncrease` is issued with
        - `Id = RaceId`
        - `AbilityScoreIncrease = ValidAbilityScoreIncrease`
3. Then expect event(s):
    - `RaceAbilityScoreIncreaseSet` with
        - `Id = RaceId`
        - `AbilityScoreIncrease = ValidAbilityScoreIncrease`
        
### Can set Race ability score increase unchanged
1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
    - `RaceAbilityScoreIncreaseSet` with
        - `Id = RaceId`
        - `AbilityScoreIncrease = ValidAbilityScoreIncrease`
2. When command:
    - `SetRaceAbilityScoreIncrease` is issued with
        - `Id = RaceId`
        - `AbilityScoreIncrease = ValidAbilityScoreIncrease`
3. Then expect event(s):
    - None

### Cannot set Race ability score increase with `Other` tokens equal to or more than available abilities
1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
2. When command:
    - `SetRaceAbilityScoreIncrease` is issued with
        - `Id = RaceId`
        - `AbilityScoreIncrease = InvalidAbilityScoreIncrease`
3. Then expect exception:
    - `TooManyOtherAbilityScoreIncreaseTokens`

### Cannot set Race ability score increase with invalid token structure
1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
2. When command:
    - `SetRaceAbilityScoreIncrease` is issued with
        - `Id = RaceId`
        - `AbilityScoreIncrease = InvalidAbilityScoreIncreaseTokenStructure`
3. Then expect exception:
    - `InvalidAbilityScoreIncreaseTokenStructure`

### Cannot set Race ability score increase with invalid token
1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
2. When command:
    - `SetRaceAbilityScoreIncrease` is issued with
        - `Id = RaceId`
        - `AbilityScoreIncrease = InvalidAbilityScoreIncreaseToken`
3. Then expect exception:
    - `InvalidAbilityScoreIncreaseToken`

### Cannot set uncreated Race ability score increase
1. Given event(s):
    - None
2. When command:
    - `SetRaceAbilityScoreIncrease` is issued with
        - `Id = RaceId`
        - `AbilityScoreIncrease = ValidAbilityScoreIncrease`
3. Then expect exception:
    - `RaceDoesNotExist`

## Race Age
### Can set Race age
1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
2. When command:
    - `SetRaceAge` is issued with
        - `Id = RaceId`
        - `MaturityAge = MaturityAge1`
        - `LifeExpectency = LifeExpectencyAge1`
3. Then expect event(s):
    - `RaceMaturityAgeSet` with
        - `Id = RaceId`
        - `MaturityAge = MaturityAge1`
    - `RaceLifeExpectancySet` with
        - `Id = RaceId`
        - `LifeExpectency = LifeExpectencyAge1`

### Can set Race age unchanged
1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
    - `RaceMaturityAgeSet` with
        - `Id = RaceId`
        - `MaturityAge = MaturityAge1`
    - `RaceLifeExpectancySet` with
        - `Id = RaceId`
        - `LifeExpectency = LifeExpectencyAge1`
2. When command:
    - `SetRaceAge` is issued with
        - `Id = RaceId`
        - `MaturityAge = MaturityAge1`
        - `LifeExpectency = LifeExpectencyAge1`
3. Then expect event(s):
    - None

### Can set Race with same life expectency
1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
    - `RaceMaturityAgeSet` with
        - `Id = RaceId`
        - `MaturityAge = MaturityAge1`
    - `RaceLifeExpectancySet` with
        - `Id = RaceId`
        - `LifeExpectency = LifeExpectencyAge1`
2. When command:
    - `SetRaceAge` is issued with
        - `Id = RaceId`
        - `MaturityAge = MaturityAge2`
        - `LifeExpectency = LifeExpectencyAge1`
3. Then expect event(s):
    - `RaceMaturityAgeSet` with
        - `Id = RaceId`
        - `MaturityAge = MaturityAge2`

### Can set Race with same maturity age
1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
    - `RaceMaturityAgeSet` with
        - `Id = RaceId`
        - `MaturityAge = MaturityAge1`
    - `RaceLifeExpectancySet` with
        - `Id = RaceId`
        - `LifeExpectency = LifeExpectencyAge1`
2. When command:
    - `SetRaceAge` is issued with
        - `Id = RaceId`
        - `MaturityAge = MaturityAge1`
        - `LifeExpectency = LifeExpectencyAge2`
3. Then expect event(s):
    - `RaceLifeExpectancySet` with
        - `Id = RaceId`
        - `LifeExpectency = LifeExpectencyAge2`

### Cannot set Race with maturity age equal or greater than life expectency
1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
2. When command:
    - `SetRaceAge` is issued with
        - `Id = RaceId`
        - `MaturityAge = MaturityAge2`
        - `LifeExpectency = LifeExpectencyAge2`
3. Then expect exception:
    - `RaceMaturityAgeExceedsLifeExpectency`

### Cannot set Race maturity age less than one
1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
2. When command:
    - `SetRaceAge` is issued with
        - `Id = RaceId`
        - `MaturityAge = ZeroAge`
        - `LifeExpectency = LifeExpectencyAge1`
3. Then expect exception:
    - `RaceMaturityAgeTooSmall`

### Cannot set uncreated Race age
1. Given event(s):
    - None
2. When command:
    - `SetRaceAge` is issued with
        - `Id = RaceId`
        - `MaturityAge = MaturityAge2`
        - `LifeExpectency = LifeExpectencyAge2`
3. Then expect exception:
    - `RaceDoesNotExist`

## Race Alignment
### Can set Race alignment
1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
2. When command:
    - `SetRaceAlignment` is issued with
        - `Id = RaceId`
        - `Orthodoxy = Lawful`
        - `Morality = Good`
3. Then expect event(s):
    - `RaceOrthodoxySet` with
        - `Id = RaceId`
        - `Orthodoxy = Lawful`
    - `RaceMoralitySet` with
        - `Id = RaceId`
        - `Morality = Good`

### Can set Race alignment unchanged
1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
    - `RaceOrthodoxySet` with
        - `Id = RaceId`
        - `Orthodoxy = Lawful`
    - `RaceMoralitySet` with
        - `Id = RaceId`
        - `Morality = Good`
2. When command:
    - `SetRaceAlignment` is issued with
        - `Id = RaceId`
        - `Orthodoxy = Lawful`
        - `Morality = Good`
3. Then expect event(s):
    - None

### Can set Race alignment with same morality
1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
    - `RaceOrthodoxySet` with
        - `Id = RaceId`
        - `Orthodoxy = Lawful`
    - `RaceMoralitySet` with
        - `Id = RaceId`
        - `Morality = Good`
2. When command:
    - `SetRaceAlignment` is issued with
        - `Id = RaceId`
        - `Orthodoxy = Chaotic`
        - `Morality = Good`
3. Then expect event(s):
    - `RaceOrthodoxySet` with
        - `Id = RaceId`
        - `Orthodoxy = Chaotic`

### Can set Race alignment with same orthodoxy
1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
    - `RaceOrthodoxySet` with
        - `Id = RaceId`
        - `Orthodoxy = Lawful`
    - `RaceMoralitySet` with
        - `Id = RaceId`
        - `Morality = Good`
2. When command:
    - `SetRaceAlignment` is issued with
        - `Id = RaceId`
        - `Orthodoxy = Lawful`
        - `Morality = Evil`
3. Then expect event(s):
    - `RaceMoralitySet` with
        - `Id = RaceId`
        - `Morality = Evil`


### Cannot set Race alignment with outer spectrum orthodoxy
1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
2. When command:
    - `SetRaceAlignment` is issued with
        - `Id = RaceId`
        - `Orthodoxy = OverlyLawful`
        - `Morality = Good`
3. Then expect exception:
    - `RaceOrthodoxyOutsideAllowedSpectrum`

1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
2. When command:
    - `SetRaceAlignment` is issued with
        - `Id = RaceId`
        - `Orthodoxy = OverlyChaotic`
        - `Morality = Good`
3. Then expect exception:
    - `RaceOrthodoxyOutsideAllowedSpectrum`

### Cannot set Race alignment with outer spectrum morality
1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
2. When command:
    - `SetRaceAlignment` is issued with
        - `Id = RaceId`
        - `Orthodoxy = Lawful`
        - `Morality = OverlyGood`
3. Then expect exception:
    - `RaceOrthodoxyOutsideAllowedSpectrum`

1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
2. When command:
    - `SetRaceAlignment` is issued with
        - `Id = RaceId`
        - `Orthodoxy = Lawful`
        - `Morality = OverlyEvil`
3. Then expect exception:
    - `RaceOrthodoxyOutsideAllowedSpectrum`

### Cannot set uncreated Race age
1. Given event(s):
    - None
2. When command:
    - `SetRaceAlignment` is issued with
        - `Id = RaceId`
        - `Orthodoxy = Lawful`
        - `Morality = Good`
3. Then expect exception:
    - `RaceDoesNotExist`

## Race Size
### Can set Race size
1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
2. When command:
    - `SetRaceSize` is issued with
        - `Id = RaceId`
        - `SizeCategory = MediumSize`
        - `BaseWeight = HundredAndTenPounds`
        - `WeightModifier = TwoTenSidedDie`
        - `BaseHeight = FourFootEight`
        - `HeightModifier = ThreeFourSidedDie`
3. Then expect event(s):
    - `RaceSizeCategorySet` with
        - `Id = RaceId`
        - `SizeCategory = MediumSize`
    - `RaceBaseWeightSet` with
        - `Id = RaceId`
        - `BaseWeight = HundredAndTenPounds`
    - `RaceWeightModifiertSet` with
        - `Id = RaceId`
        - `WeightModifier = TwoTenSidedDie`
    - `RaceBaseHeightSet` with
        - `Id = RaceId`
        - `BaseHeight = FourFootEight`
    - `RaceHeightModifierSet` with
        - `Id = RaceId`
        - `HeightModifier = ThreeFourSidedDie`

### Can set Race size with unchanged values
1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
    - `RaceSizeCategorySet` with
        - `Id = RaceId`
        - `SizeCategory = MediumSize`
    - `RaceBaseWeightSet` with
        - `Id = RaceId`
        - `BaseWeight = HundredAndTenPounds`
    - `RaceWeightModifiertSet` with
        - `Id = RaceId`
        - `WeightModifier = TwoTenSidedDie`
    - `RaceBaseHeightSet` with
        - `Id = RaceId`
        - `BaseHeight = FourFootEight`
    - `RaceHeightModifierSet` with
        - `Id = RaceId`
        - `HeightModifier = ThreeFourSidedDie`
2. When command:
    - `SetRaceSize` is issued with
        - `Id = RaceId`
        - `SizeCategory = MediumSize`
        - `BaseWeight = HundredAndTenPounds`
        - `WeightModifier = TwoTenSidedDie`
        - `BaseHeight = FourFootEight`
        - `HeightModifier = ThreeFourSidedDie`
3. Then expect event(s):
    - None

1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
    - `RaceSizeCategorySet` with
        - `Id = RaceId`
        - `SizeCategory = MediumSize`
    - `RaceBaseWeightSet` with
        - `Id = RaceId`
        - `BaseWeight = HundredAndTenPounds`
    - `RaceWeightModifiertSet` with
        - `Id = RaceId`
        - `WeightModifier = TwoTenSidedDie`
    - `RaceBaseHeightSet` with
        - `Id = RaceId`
        - `BaseHeight = FourFootEight`
    - `RaceHeightModifierSet` with
        - `Id = RaceId`
        - `HeightModifier = ThreeFourSidedDie`
2. When command:
    - `SetRaceSize` is issued with
        - `Id = RaceId`
        - `SizeCategory = LargeSize`
        - `BaseWeight = HundredAndTenPounds`
        - `WeightModifier = TwoTenSidedDie`
        - `BaseHeight = FourFootEight`
        - `HeightModifier = ThreeFourSidedDie`
3. Then expect event(s):
    - `RaceSizeCategorySet` with
        - `Id = RaceId`
        - `SizeCategory = LargeSize`

1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
    - `RaceSizeCategorySet` with
        - `Id = RaceId`
        - `SizeCategory = MediumSize`
    - `RaceBaseWeightSet` with
        - `Id = RaceId`
        - `BaseWeight = HundredAndTenPounds`
    - `RaceWeightModifiertSet` with
        - `Id = RaceId`
        - `WeightModifier = TwoTenSidedDie`
    - `RaceBaseHeightSet` with
        - `Id = RaceId`
        - `BaseHeight = FourFootEight`
    - `RaceHeightModifierSet` with
        - `Id = RaceId`
        - `HeightModifier = ThreeFourSidedDie`
2. When command:
    - `SetRaceSize` is issued with
        - `Id = RaceId`
        - `SizeCategory = MediumSize`
        - `BaseWeight = SeventyFivePounds`
        - `WeightModifier = TwoTenSidedDie`
        - `BaseHeight = FourFootEight`
        - `HeightModifier = ThreeFourSidedDie`
3. Then expect event(s):
    - `RaceBaseWeightSet` with
        - `Id = RaceId`
        - `BaseWeight = SeventyFivePounds`

1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
    - `RaceSizeCategorySet` with
        - `Id = RaceId`
        - `SizeCategory = MediumSize`
    - `RaceBaseWeightSet` with
        - `Id = RaceId`
        - `BaseWeight = HundredAndTenPounds`
    - `RaceWeightModifiertSet` with
        - `Id = RaceId`
        - `WeightModifier = TwoTenSidedDie`
    - `RaceBaseHeightSet` with
        - `Id = RaceId`
        - `BaseHeight = FourFootEight`
    - `RaceHeightModifierSet` with
        - `Id = RaceId`
        - `HeightModifier = ThreeFourSidedDie`
2. When command:
    - `SetRaceSize` is issued with
        - `Id = RaceId`
        - `SizeCategory = MediumSize`
        - `BaseWeight = HundredAndTenPounds`
        - `WeightModifier = ThreeFourSidedDie`
        - `BaseHeight = FourFootEight`
        - `HeightModifier = ThreeFourSidedDie`
3. Then expect event(s):
    - `RaceWeightModifiertSet` with
        - `Id = RaceId`
        - `WeightModifier = ThreeFourSidedDie`

1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
    - `RaceSizeCategorySet` with
        - `Id = RaceId`
        - `SizeCategory = MediumSize`
    - `RaceBaseWeightSet` with
        - `Id = RaceId`
        - `BaseWeight = HundredAndTenPounds`
    - `RaceWeightModifiertSet` with
        - `Id = RaceId`
        - `WeightModifier = TwoTenSidedDie`
    - `RaceBaseHeightSet` with
        - `Id = RaceId`
        - `BaseHeight = FourFootEight`
    - `RaceHeightModifierSet` with
        - `Id = RaceId`
        - `HeightModifier = ThreeFourSidedDie`
2. When command:
    - `SetRaceSize` is issued with
        - `Id = RaceId`
        - `SizeCategory = MediumSize`
        - `BaseWeight = HundredAndTenPounds`
        - `WeightModifier = TwoTenSidedDie`
        - `BaseHeight = ThreeFootSeven`
        - `HeightModifier = ThreeFourSidedDie`
3. Then expect event(s):
    - `RaceBaseHeightSet` with
        - `Id = RaceId`
        - `BaseHeight = ThreeFootSeven`

1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
    - `RaceSizeCategorySet` with
        - `Id = RaceId`
        - `SizeCategory = MediumSize`
    - `RaceBaseWeightSet` with
        - `Id = RaceId`
        - `BaseWeight = HundredAndTenPounds`
    - `RaceWeightModifiertSet` with
        - `Id = RaceId`
        - `WeightModifier = TwoTenSidedDie`
    - `RaceBaseHeightSet` with
        - `Id = RaceId`
        - `BaseHeight = FourFootEight`
    - `RaceHeightModifierSet` with
        - `Id = RaceId`
        - `HeightModifier = ThreeFourSidedDie`
2. When command:
    - `SetRaceSize` is issued with
        - `Id = RaceId`
        - `SizeCategory = MediumSize`
        - `BaseWeight = HundredAndTenPounds`
        - `WeightModifier = TwoTenSidedDie`
        - `BaseHeight = FourFootEight`
        - `HeightModifier = TwoTenSidedDie`
3. Then expect event(s):
    - `RaceHeightModifierSet` with
        - `Id = RaceId`
        - `HeightModifier = TwoTenSidedDie`

### Cannot set uncreated Race size
1. Given event(s):
    - None
2. When command:
    - `SetRaceSize` is issued with
        - `Id = RaceId`
        - `SizeCategory = MediumSize`
        - `BaseWeight = HundredAndTenPounds`
        - `WeightModifier = TwoTenSidedDie`
        - `BaseHeight = FourFootEight`
        - `HeightModifier = ThreeFourSidedDie`
3. Then expect exception:
    - `RaceDoesNotExist`

# Race Test

A suite of tests verifies the behavioural functionality of the [`RaceAggregate`]()

## Index
1. [Setup](#setup)
2. [Race Creation](#race-creation)
3. [Race Details](#race-details)

## Setup
### The set of values used in determining whether expected outcomes are achieved.

Alias                   |   Value           |
------------------------|-------------------|
**`RaceId`**            | '_uuid.UUID_'     |
**`SubraceId`**         | '_uuid.UUID_'     |
**`RaceName1`**         | '_Test Race 1_'   |
**`RaceName2`**         | '_Test Race 2_'   |
**`RaceDescription1`**  | '_Description 1_' |
**`RaceDescription2`**  | '_Description 2_' |
**`SubraceName1`**      | '_Test Subrace 1_'|
**`SubraceName2`**      | '_Test Subrace 2_'|

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
        - `Id = SubraceId`
        - `Name = RaceName1`
    - `RaceDescriptionSet` with
        - `Id = SubraceId`
        - `Description = RaceDescription1`

### Can set Race details with same name
1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
    - `RaceNameSet` with
        - `Id = SubraceId`
        - `Name = RaceName1`
    - `RaceDescriptionSet` with
        - `Id = SubraceId`
        - `Description = RaceDescription1`
2. When command:
    - `SetRaceDetails` is issued with
        - `Id = RaceId`
        - `Name = RaceName1`
        - `Description = RaceDescription2`
3. Then expect event(s):
    - `RaceDescriptionSet` with
        - `Id = SubraceId`
        - `Description = RaceDescription2`

### Can set Race details with same description
1. Given event(s):
    - `RaceCreated` with 
        - `Id = RaceId`
        - `BaseRaceId = None`
    - `RaceNameSet` with
        - `Id = SubraceId`
        - `Name = RaceName1`
    - `RaceDescriptionSet` with
        - `Id = SubraceId`
        - `Description = RaceDescription1`
2. When command:
    - `SetRaceDetails` is issued with
        - `Id = RaceId`
        - `Name = RaceName2`
        - `Description = RaceDescription1`
3. Then expect event(s):
    - `RaceNameSet` with
        - `Id = SubraceId`
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
    - `RaceCannotBeBasedOnSelf`

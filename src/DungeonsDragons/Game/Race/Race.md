# Race

### Inherits from:
- [`Aggregate`](../../../Infrastructure/Aggregate.md)

## Properties
### Public
- Name ( `String` )
- Description ( `String` )
- Ability Score Increase ( `Object[]` )
- Age ( `Number[2]` )
- Alignment ( `Number[2]` )
- Size ( `Enum` )
- Speed ( `Number` )
- Languages ( `Enum[]` )
- Subraces ( `Object[]` )
- Spells ( `Ability[]` )

### Private
- Active ( `Boolean` )
- Base Race ( `Race` )

## Command Handlers
- Create Race
- Activate Race
- Deactivate Race
- Set Race Ability Score
- Set Race Age
- Set Race Alignment
- Set Race Description
- Set Race Name
- Set Race Size
- Set Race Speed
- Add Race Abilitiy
- Remove Race Abilitiy
- Add Race Language
- Remove Race Language
- Add Subrace
- Remove Subrace

## Event Handlers
- Race Created
- Race Activated
- Race Deactivated
- Race Ability Score Set
- Race Age Set
- Race Alignment Set
- Race Description Set
- Race Name Set
- Race Size Set
- Race Speed Set
- Race Abilitiy Added
- Race Abilitiy Removed
- Race Language Added
- Race Language Removed
- Subrace Added
- Subrace Removed
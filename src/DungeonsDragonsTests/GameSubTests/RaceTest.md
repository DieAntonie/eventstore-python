# Race Test

A suite of tests verifies the behavioural functionality of the [`RaceAggregate`]()

## Index
1. [Setup](#setup)
2. test_can_create_race
3. test_cannot_create_race_more_than_once
4. test_can_change_race_name
5. test_can_change_race_name_more_than_once
6. test_cannot_change_uncreated_race_name
7. test_cannot_change_race_name_to_current_race_name
8. test_can_add_subrace
9. test_cannot_add_subrace_to_uncreated_race
10. test_can_add_multiple_subraces
11. test_cannot_add_same_subrace_more_than_once
12. test_can_remove_subrace
13. test_can_add_removed_subrace
14. test_cannot_removed_subrace_more_than_once
15. test_can_rename_subrace
16. test_can_rename_subrace_more_than_once
17. test_cannot_rename_unadded_subrace
18. test_can_set_race_ability_modifiers

## Setup
### The set of values used in determining whether expected outcomes are achieved.

Alias               |   Value           |
--------------------|-------------------|
**`RaceName1`**     | '_Test Race 1_'   |
**`RaceName2`**     | '_Test Race 2_'   |
**`SubraceName1`**  | '_Test Subrace 1_'|
**`SubraceName2`**  | '_Test Subrace 2_'|

def test_can_create_race(self):
self.Test(
    self.Given(),
    self.When(
        CreateRace(
            self.testId,
            self.RaceName1
        )
    ),
    self.Then(
        RaceCreated(
            self.testId,
            self.RaceName1
        )
    )
)

def test_cannot_create_race_more_than_once(self):
self.Test(
    self.Given(
        RaceCreated(
            self.testId,
            self.RaceName1
        )
    ),
    self.When(
        CreateRace(
            self.testId,
            self.RaceName1
        )
    ),
    self.ThenFailWith(RaceAlreadyCreated)
)

def test_can_change_race_name(self):
self.Test(
    self.Given(
        RaceCreated(
            self.testId,
            self.RaceName1
        )
    ),
    self.When(
        ChangeRaceName(
            self.testId,
            self.RaceName2
        )
    ),
    self.Then(
        RaceNameChanged(
            self.testId,
            self.RaceName1,
            self.RaceName2
        )
    )
)

def test_can_change_race_name_more_than_once(self):
self.Test(
    self.Given(
        RaceCreated(
            self.testId,
            self.RaceName1
        ),
        RaceNameChanged(
            self.testId,
            self.RaceName1,
            self.RaceName2
        )
    ),
    self.When(
        ChangeRaceName(
            self.testId,
            self.RaceName1
        )
    ),
    self.Then(
        RaceNameChanged(
            self.testId,
            self.RaceName2,
            self.RaceName1
        )
    )
)

def test_cannot_change_uncreated_race_name(self):
self.Test(
    self.Given(),
    self.When(
        ChangeRaceName(
            self.testId,
            self.RaceName1
        )
    ),
    self.ThenFailWith(RaceDoesNotExist)
)

def test_cannot_change_race_name_to_current_race_name(self):
self.Test(
    self.Given(
        RaceCreated(
            self.testId,
            self.RaceName1
        )
    ),
    self.When(
        ChangeRaceName(
            self.testId,
            self.RaceName1
        )
    ),
    self.ThenFailWith(RaceNameDoesNotDiffer)
)

def test_can_add_subrace(self):
self.Test(
    self.Given(
        RaceCreated(
            self.testId,
            self.RaceName1
        )
    ),
    self.When(
        Addsubrace(
            self.testId,
            self.subraceName1
        )
    ),
    self.Then(
        subraceAdded(
            self.testId,
            self.subraceName1
        )
    )
)

def test_cannot_add_subrace_to_uncreated_race(self):
self.Test(
    self.Given(),
    self.When(
        Addsubrace(
            self.testId,
            self.subraceName1
        )
    ),
    self.ThenFailWith(RaceDoesNotExist)
)

def test_can_add_multiple_subraces(self):
self.Test(
    self.Given(
        RaceCreated(
            self.testId,
            self.RaceName1
        ),
        subraceAdded(
            self.testId,
            self.subraceName1
        )
    ),
    self.When(
        Addsubrace(
            self.testId,
            self.subraceName2
        )
    ),
    self.Then(
        subraceAdded(
            self.testId,
            self.subraceName2
        )
    )
)

def test_cannot_add_same_subrace_more_than_once(self):
self.Test(
    self.Given(
        RaceCreated(
            self.testId,
            self.RaceName1
        ),
        subraceAdded(
            self.testId,
            self.subraceName1
        )
    ),
    self.When(
        Addsubrace(
            self.testId,
            self.subraceName1
        )
    ),
    self.ThenFailWith(subraceAlreadyExists)
)

def test_can_remove_subrace(self):
self.Test(
    self.Given(
        RaceCreated(
            self.testId,
            self.RaceName1
        ),
        subraceAdded(
            self.testId,
            self.subraceName1
        )
    ),
    self.When(
        Removesubrace(
            self.testId,
            self.subraceName1
        )
    ),
    self.Then(
        subraceRemoved(
            self.testId,
            self.subraceName1
        )
    )
)

def test_can_add_removed_subrace(self):
self.Test(
    self.Given(
        RaceCreated(
            self.testId,
            self.RaceName1
        ),
        subraceAdded(
            self.testId,
            self.subraceName1
        ),
        subraceRemoved(
            self.testId,
            self.subraceName1
        )
    ),
    self.When(
        Addsubrace(
            self.testId,
            self.subraceName1
        )
    ),
    self.Then(
        subraceAdded(
            self.testId,
            self.subraceName1
        )
    )
)

def test_cannot_removed_subrace_more_than_once(self):
self.Test(
    self.Given(
        RaceCreated(
            self.testId,
            self.RaceName1
        ),
        subraceAdded(
            self.testId,
            self.subraceName1
        ),
        subraceRemoved(
            self.testId,
            self.subraceName1
        )
    ),
    self.When(
        Removesubrace(
            self.testId,
            self.subraceName1
        )
    ),
    self.ThenFailWith(subraceDoesNotExists)
)

def test_can_rename_subrace(self):
self.Test(
    self.Given(
        RaceCreated(
            self.testId,
            self.RaceName1
        ),
        subraceAdded(
            self.testId,
            self.subraceName1
        )
    ),
    self.When(
        Renamesubrace(
            self.testId,
            self.subraceName1,
            self.subraceName2
        )
    ),
    self.Then(
        subraceRenamed(
            self.testId,
            self.subraceName1,
            self.subraceName2
        )
    )
)

def test_can_rename_subrace_more_than_once(self):
self.Test(
    self.Given(
        RaceCreated(
            self.testId,
            self.RaceName1
        ),
        subraceAdded(
            self.testId,
            self.subraceName1
        ),
        subraceRenamed(
            self.testId,
            self.subraceName1,
            self.subraceName2
        )
    ),
    self.When(
        Renamesubrace(
            self.testId,
            self.subraceName2,
            self.subraceName1
        )
    ),
    self.Then(
        subraceRenamed(
            self.testId,
            self.subraceName2,
            self.subraceName1
        )
    )
)

def test_cannot_rename_unadded_subrace(self):
self.Test(
    self.Given(
        RaceCreated(
            self.testId,
            self.RaceName1
        )
    ),
    self.When(
        Renamesubrace(
            self.testId,
            self.subraceName1,
            self.subraceName2
        )
    ),
    self.ThenFailWith(subraceDoesNotExists)
)

def test_can_set_race_ability_modifiers(self):
self.Test(
    self.Given(
        RaceCreated(
            self.testId,
            self.RaceName1
        )
    ),
    self.When(
        SetRaceAbilityModifiers(
            self.testId,
            []
        )
    ),
    self.Then(
        RaceAbilityModifiersSet(
            self.testId,
            []
        )
    )
)

if __name__ == '__main__':
unittest.main()
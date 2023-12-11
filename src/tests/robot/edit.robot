*** Settings ***
Resource  resource.robot
Test Setup  Clear

# Käyttäjänä voin muokata lisäämiäni viitteitä

*** Test Cases ***
Edit NonExisting Source
    Input Command  9
    Input Command  Kirjailija23
    Run
    Output Should Contain  Citation key Kirjailija23 did not match any references\n

Edit Source And Make Changes
    Create Book Source
    Input Command  9
    Input Command  Kirjailija23
    Input Command  ${EMPTY}
    Input Command  ${EMPTY}
    Input Command  2024
    Input Command  ${EMPTY}
    Input Command  q
    Run
    Output Should Contain  Reference edited ( Kirjailija23 --> Kirjailija24 )

Edit Source With No Changes
    Create Book Source
    Input Command  9
    Input Command  Kirjailija23
    Input Command  ${EMPTY}
    Input Command  ${EMPTY}
    Input Command  ${EMPTY}
    Input Command  ${EMPTY}
    Input Command  q
    Run
    Output Should Contain  Reference edited ( Kirjailija23 --> Kirjailija23 )

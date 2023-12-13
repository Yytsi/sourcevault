*** Settings ***
Resource  resource.robot
Test Setup  Clear

# Käyttäjänä pystyn listaamaan lisätyt viitteet

*** Test Cases ***
List Correct Keys
    Create Book Source
    Input Command  4
    Input Command  11
    Run
    Output Should Contain  Kirjailija23
    Output Should Contain  There exists 1 citation keys:

List No Keys
    Input Command  4
    Input Command  11
    Run
    Output Should Contain  There exists 0 citation keys:

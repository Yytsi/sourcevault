*** Settings ***
Resource  resource.robot
Test Setup  Clear

# Käyttäjänä voin hakea dataa DOI-tunnisteen perusteella

*** Test Cases ***
Create Source Using DOI
    Input Command  8
    Input Command  10.1007/s00146-021-01245-6
    Run
    Output Should Contain  Source added!


*** Settings ***
Library  ../../AppLibrary.py

*** Keywords ***
Input Command
    [Arguments]  ${command}
    Input  ${command}

Create Book Source
    Input Command  1
    Input Command  1
    Input Command  Kirjailija
    Input Command  Otsikko
    Input Command  2023
    Input Command  Julkaisija
    Input Command  q

Source As Text
    [Arguments]   ${citation_key}
    ${string}=  Get String  ${citation_key}
    RETURN  ${string}

Run
    Input Command  10
    Run Application

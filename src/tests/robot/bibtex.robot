*** Settings ***
Resource  resource.robot
Test Setup  Clear

# kayttäjä voi tarkastella lähdeviitteitä BibTeX modossa

#*** Test Cases ***
Bibtex File Is Created
    Create Book Source
    Input Command  3
    Run
    ${location}=  Get Bibtex Location
    Output Should Contain  ${location}

Empty Bibtext File Is Not Created
    Input Command  3
    Run
    Output Should Contain  no sources yet :/ \n

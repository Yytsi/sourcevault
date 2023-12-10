*** Settings ***
Resource  resource.robot
Test Setup  Clear

# Käyttäjänä pystyn valitsemaan lähteen tyypin (Book, Article, Inproceedings)
# Käyttäjänä voin lisätä myös misc ja PhD-thesis tyyppisiä viitteitä

*** Test Cases ***
Add Article With Valid Information
    Input Command  1
    Input Command  2
    Input Command  Kirjailija
    Input Command  Otsikko
    Input Command  Lehti
    Input Command  2023
    Input Command  20
    Input Command  20
    Input Command  q
    Run
    Output Should Contain  Reference added


Add Inproceeding With Valid Information
    Input Command  1
    Input Command  3
    Input Command  Kirjailija
    Input Command  Otsikko
    Input Command  2023
    Input Command  Kirja
    Input Command  q
    Run
    Output Should Contain  Reference added

Add Misc With Valid Information
    Input Command  1
    Input Command  4
    Input Command  Kirjailija
    Input Command  Otsikko
    Input Command  Julkaisu
    Input Command  2023
    Input Command  Huom
    Input Command  q
    Run
    Output Should Contain  Reference added

Add Phd With Valid Information
    Input Command  1
    Input Command  5
    Input Command  Kirjailija
    Input Command  Otsikko
    Input Command  2023
    Input Command  Koulu
    Input Command  Osoite
    Input Command  12
    Input Command  q
    Run
    Output Should Contain  Reference added


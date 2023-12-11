*** Settings ***
Resource  resource.robot

# Käyttäjänä pystyn suodattamaan viitteitä kirjoittajan tai vuosiluvun perusteella
# käyttäjänä voin filtteroida ja tägätä lisäämiään lähdeliitteitä

*** Test Cases ***
Create Source With Tag
    Clear
    Input Command  1
    Input Command  1
    Input Command  Kirjailija
    Input Command  Otsikko
    Input Command  2023
    Input Command  Julkaisija
    Input Command  Tägi1
    Input Command  q
    Run
    Output Should Contain  Reference added

Find Source With Existing Tag
    Input Command  7
    Input Command  3
    Input Command  Tägi1
    Input Command  4
    Run
    ${string}=  Source As Text  Kirjailija23
    Output Should Contain  ${string}

Find No Sources With NonExisting Tag
    Input Command  7
    Input Command  3
    Input Command  Tägi2
    Input Command  4
    Run
    Output Should Contain  No sources found with value Tägi2!

Find Source With Existing Author
    Input Command  7
    Input Command  1
    Input Command  Kirjailija
    Input Command  4
    Run
    ${string}=  Source As Text  Kirjailija23
    Output Should Contain  ${string}

Find No Sources With NonExisting Author
    Input Command  7
    Input Command  1
    Input Command  Kirjailija2
    Input Command  4
    Run
    Output Should Contain  No sources found with value Kirjailija2!

Find Source With Existing Year
    Input Command  7
    Input Command  2
    Input Command  2023
    Input Command  4
    Run
    ${string}=  Source As Text  Kirjailija23
    Output Should Contain  ${string}

Find No Sources With NonExisting Year
    Input Command  7
    Input Command  2
    Input Command  2024
    Input Command  4
    Run
    Output Should Contain  No sources found with value 2024!

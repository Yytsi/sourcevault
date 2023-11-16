def convert_to_bibtex(type, **fields):
    """
    Luo BibTeX-viitteen.

    :param entry_type: Viitteen tyyppi, esim. 'article', 'book'.
    :param identifier: Ainutlaatuinen tunniste viitteelle.
    :param fields: Avain-arvo -parit, jotka kuvaavat viitettä (esim. author='Martin, Robert', title='Kirjan nimi').
    :return: BibTeX merkkijonomuodossa.
    """
    
    names = fields["author"].split(" and ")
    identifier = "".join(s.split()[-1][0] for s in names)

    if len(names) == 1:
        identifier = names[0].split(", ")[0]
    
    identifier += fields["year"][-2:]
    bibtex_str = f"@{type}{{{identifier}}},\n"
    for field, value in fields.items():
        bibtex_str += f"    {field} = {{{value}}},\n"
    return bibtex_str + "}\n"

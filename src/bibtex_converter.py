"""Moduuli joka vastaa bibtex formaattiin kääntämisestä"""


def convert_to_bibtex(source_type, **fields):
    """
    Luo BibTeX-viitteen.

    :param type: Viitteen tyyppi, esim. 'article', 'book'.
    :param fields: Avain-arvo -parit, jotka kuvaavat viitettä (esim. author='Martin, Robert', title='Kirjan nimi').
    :return: BibTeX merkkijonomuodossa.
    """
    names = str(fields.get("author")).split(" and ")
    identifier = "".join(s.split()[-1][0] for s in names)
    if len(names) == 1:
        identifier = names[0].split(", ")[0]

    identifier += str(fields.get("year"))[-2:]
    bibtex_str = f"@{source_type}" + "{" + f"{identifier},\n"
    fields_length = len(fields.items() - 1)
    for i, (field, value) in enumerate(fields.items()):
        end_char = " ,"[i != fields_length]
        bibtex_str += f"    {field} = {{{value}}}{end_char}\n"
    return bibtex_str + "}\n\n"

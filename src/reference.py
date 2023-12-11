"""Moduuli joka muodostaa viiteoliot"""


class Reference:
    """
    Kuvaus luokan päätehtävästä
    ...

    Attributes
    ----------
    attr : tyyppi
        Kuvaus

    Methods
    -------
    method():
        kuvaus.
    """

    def __init__(self, reference_type, citation_key="", tags=None, **fields):
        """
        Luokan konstruktori.
        ...

        Parameters
        ----------
        muuttuja : tyyppi
            kuvaus
        """
        self.reference_type = reference_type
        self.citation_key = citation_key
        self.fields = fields
        self.tags = tags or []

    def generate_citation_key(self):
        """
        Kuvaus Funktion toiminnalisuudesta
        ...

        Parameters
        ----------
        muuttuja : tyyppi
            kuvaus
        """
        names = str(self.fields.get("author")).split(" and ")
        citation_key = "".join(s.split()[-1][0] for s in names)

        if len(names) == 1:
            citation_key = names[0].split(", ")[0]

        citation_key += str(self.fields.get("year"))[-2:]
        return citation_key

    def __str__(self):
        """
        Kuvaus Funktion toiminnalisuudesta
        ...

        Parameters
        ----------
        muuttuja : tyyppi
            kuvaus
        """
        op = f"{self.citation_key}, {self.reference_type}:\n"
        for k, v in self.fields.items():
            op += f"{k} = {v}\n"
        if len(self.tags) == 0:
            op += "No tags associated.\n"
        else:
            for i, tag in enumerate(self.tags):
                op += f"Tag {i+1}: {tag}\n"
        return op

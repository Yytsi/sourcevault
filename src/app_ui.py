"""Moduuli joka vastaa käyttäjän näkemästä käyttöliittymästä"""
import os
from reference import Reference
from doi_seacher import DOISearcher


class AppUI:
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

    def __init__(self, root):
        """
        Luokan konstruktori.
        ...

        Parameters
        ----------
        muuttuja : tyyppi
            kuvaus
        """
        self.root = root

    def run_app(self):
        """
        Kuvaus Funktion toiminnalisuudesta
        ...

        Parameters
        ----------
        muuttuja : tyyppi
            kuvaus
        """
        if self.root.read_sources_from_database() is True:
            print("connected to bucket!")
        else:
            # kysy käyttäjältä halutaanko configuroida bucketti
            print("\nWould you like to connect to an AWS bucket?")
            print('This can be done with the "configure bucket" command')
            print(
                "(this will overwrite the current database, for more info, see guide in readme)"
            )

        while True:
            command = self.root.io_handler.read_input(
                (
                    "\n1 : create new\n2 : list sources as text\n3 : create bibtext\n4 : list all citation keys\n"
                    "5 : show based on citation key\n6 : delete based on citation key\n7 : filter references"
                    "\n8 : find reference with DOI\n9 : edit based on citation key\n10 : configure bucket\n11 : exit program\n"
                )
            )

            match command:
                case "1":
                    self.create_new()

                case "2":
                    self.list_sources()

                case "3":
                    self.convert_to_bibtex()

                case "4":
                    self.list_citation_keys()

                case "5":
                    self.show_by_citation_keys()

                case "6":
                    self.delete_by_key()

                case "7":
                    self.search_by_key()

                case "8":
                    self.search_by_doi()

                case "9":
                    self.edit_by_key()

                case "10":
                    self.create_env()

                case "11":
                    # Lopetus
                    break

        self.root.update_database()

    def search_by_doi(self):
        """
        Kuvaus Funktion toiminnalisuudesta
        ...

        Parameters
        ----------
        muuttuja : tyyppi
            kuvaus
        """
        doi = self.root.io_handler.read_input("Enter a DOI: ")
        ds = DOISearcher()
        ref = ds.find_by_doi(doi)
        self.root.add_source(ref)
        # TODO! Add with tags!
        self.root.io_handler.write_output("Source added!")

    def create_new(self):
        """
        Kuvaus Funktion toiminnalisuudesta
        ...

        Parameters
        ----------
        muuttuja : tyyppi
            kuvaus
        """
        # Uuden lähteen luonti

        reference_type = ""
        fields_data = {}

        while True:
            source_type = self.root.io_handler.read_input(
                "Choose source type (type a number):\n1. Book\n2. Article\n3. Inproceedings\n4. Miscellaneous\n5. Phd thesis\n6. Cancel\nChoice: "
            )
            required_fields = []
            match source_type:
                case "1":
                    required_fields = "author|title|year|publisher"
                    reference_type = "book"
                case "2":
                    required_fields = "author|title|journal|year|volume|pages"
                    reference_type = "article"
                case "3":
                    required_fields = "author|title|year|booktitle"
                    reference_type = "inproceedings"
                case "4":
                    required_fields = "author|title|howpublished|year|note"
                    reference_type = "misc"
                case "5":
                    required_fields = "author|title|year|school|address|month"
                    reference_type = "phdthesis"
                case "6":
                    return
                case default:  # pylint: disable=unused-variable
                    self.root.io_handler.write_output("Please pick a valid option")
                    continue

            for field in required_fields.split("|"):
                fields_data[field] = self.root.io_handler.read_input(
                    f"insert {field}: "
                )

            break

        ref = Reference(reference_type, **fields_data)
        ref.citation_key = ref.generate_citation_key()

        tags = []

        while True:
            # Read tags
            tag = self.root.io_handler.read_input(
                "Enter a tag or type q to stop: "
            ).strip()
            if tag == "q":
                break
            tags.append(tag)

        ref.tags = tags

        self.root.add_source(ref)

        self.root.io_handler.write_output("Reference added")

    def list_sources(self):
        """
        Kuvaus Funktion toiminnalisuudesta
        ...

        Parameters
        ----------
        muuttuja : tyyppi
            kuvaus
        """
        # Lähteiden lukeminen inhimillisessä muodossa
        if not self.root.my_sources:
            self.root.io_handler.write_output("no sources yet :/ \n")

        for i, ref in enumerate(self.root.my_sources):
            self.root.io_handler.write_output(f"Reference {i+1}:")
            self.root.io_handler.write_output(ref)
            self.root.io_handler.write_output("\n")

    def convert_to_bibtex(self):
        """
        Kuvaus Funktion toiminnalisuudesta
        ...

        Parameters
        ----------
        muuttuja : tyyppi
            kuvaus
        """
        # Bibtextiin kääntäminen
        if not self.root.my_sources:
            self.root.io_handler.write_output("no sources yet :/ \n")
        else:
            self.root.io_handler.write_output(
                f"Wrote to: {os.getcwd()}/{self.root.location} \n"
            )
            self.root.write_sources_bibtex()

    def list_citation_keys(self):
        """
        Kuvaus Funktion toiminnalisuudesta
        ...

        Parameters
        ----------
        muuttuja : tyyppi
            kuvaus
        """
        # listaa kaikki citation_keyt
        self.root.io_handler.write_output(
            f"There exists {len(self.root.my_sources)} citation keys:"
        )
        for ref in self.root.my_sources:
            self.root.io_handler.write_output(ref.citation_key)

    def show_by_citation_keys(self):
        """
        Kuvaus Funktion toiminnalisuudesta
        ...

        Parameters
        ----------
        muuttuja : tyyppi
            kuvaus
        """
        citation_key = self.root.io_handler.read_input(
            "Enter the citation key of the reference you wish to examine: "
        )
        ref = self.root.get_reference_by_key(citation_key)

        if not ref:
            self.root.io_handler.write_output(
                f"Citation key {citation_key} did not match any references\n"
            )
        else:
            self.root.io_handler.write_output(str(ref))

    def delete_by_key(self):
        """
        Kuvaus Funktion toiminnalisuudesta
        ...

        Parameters
        ----------
        muuttuja : tyyppi
            kuvaus
        """
        # poista citation_key:n perusteella
        citation_key = self.root.io_handler.read_input(
            "Enter the citation key of the reference you wish to remove: "
        ).strip()
        if self.root.remove_reference(citation_key):
            self.root.io_handler.write_output("Citation removed succesfully.")
        else:
            self.root.io_handler.write_output("No such citation.")

    def search_by_key(self):
        """
        Kuvaus Funktion toiminnalisuudesta
        ...

        Parameters
        ----------
        muuttuja : tyyppi
            kuvaus
        """

        while True:
            field_key = ""
            field_type = self.root.io_handler.read_input(
                "Choose a field to filter by (type a number):\n1. Author\n2. Year\n3. Tag\n4. Cancel\nChoice: "
            ).strip()
            match field_type:
                case "1":
                    field_key = "author"
                case "2":
                    field_key = "year"
                case "3":
                    field_key = "tags"
                case "4":
                    return
                case default:  # pylint: disable=unused-variable
                    self.root.io_handler.write_output("Please pick a valid option")
                    continue

            search = self.root.io_handler.read_input(
                "Enter the value you want to search by or q to quit: "
            ).strip()
            if search == "q":
                self.root.io_handler.write_output("exiting.")
                return

            match field_key:
                case "author":
                    found_refs = list(
                        filter(
                            lambda x: search == x.fields["author"], self.root.my_sources
                        )
                    )
                case "year":
                    found_refs = list(
                        filter(
                            lambda x: search == x.fields["year"], self.root.my_sources
                        )
                    )
                case "tags":
                    found_refs = list(
                        filter(lambda x: search in x.tags, self.root.my_sources)
                    )

            if len(found_refs) == 0:
                self.root.io_handler.write_output(
                    f"No sources found with value {search}!"
                )
            else:
                self.root.io_handler.write_output(
                    f"Found {len(found_refs)} references with: {search}\n"
                )
                for ref in found_refs:
                    self.root.io_handler.write_output(str(ref))

    def edit_by_key(self):
        """
        Muokkaa valittua viitettä.
        """
        citation_key = self.root.io_handler.read_input(
            "Enter the citation key of the reference you wish to edit: "
        ).strip()
        og_ref = self.root.get_reference_by_key(citation_key)

        if not og_ref:
            self.root.io_handler.write_output(
                f"Citation key {citation_key} did not match any references\n"
            )
            return

        self.root.io_handler.write_output(
            "Type to edit or leave blank for [original value]"
        )
        edited_data = {}

        og_tags = og_ref.tags
        reference_type = og_ref.reference_type

        for k, v in og_ref.fields.items():
            edit = self.root.io_handler.read_input(f"insert {k} [{v}]: ")
            if not edit:
                edit = v
            edited_data[k] = edit

        edited_tags = []

        for tag in og_tags:
            edited_tag = self.root.io_handler.read_input(
                f"Edit tag or type q to discard [{tag}]: "
            ).strip()
            if edited_tag == "q":
                continue
            if not edited_tag:
                edited_tag = tag
            edited_tags.append(edited_tag)

        while True:
            tag = self.root.io_handler.read_input(
                "Enter a new tag or type q to stop: "
            ).strip()
            if tag == "q":
                break
            edited_tags.append(tag)

        edited_ref = Reference(reference_type, **edited_data)
        edited_ref.tags = edited_tags
        self.root.remove_reference(citation_key)
        edited_ref.citation_key = edited_ref.generate_citation_key()
        self.root.add_source(edited_ref)
        self.root.io_handler.write_output(
            f"Reference edited ( {og_ref.citation_key} --> {edited_ref.citation_key} )"
        )

    def create_env(self):
        """
        Luo .env tiedoston.
        """
        # get input:
        bucket_name = self.root.io_handler.read_input(
            ("\nInput the name of the AWS bucket:")
        )
        access_key = self.root.io_handler.read_input(("\nInput AWS_ACCESS_KEY_ID:"))
        secret_key = self.root.io_handler.read_input(("\nInput AWS_SECRET_ACCESS_KEY:"))

        # varmista input
        print("\n Would you like to proceed with the following?:")
        print(f"AWS bucket: {bucket_name}")
        print(f"AWS_ACCESS_KEY_ID: {access_key}")
        print(f"AWS_SECRET_ACCESS_KEY: {secret_key}")

        confirm = self.root.io_handler.read_input(("y/n?: "))

        if confirm == "y":
            self.write_env(bucket_name, access_key, secret_key)
            print("\n.env updated")
            print("Restart program to connect database")

    def write_env(self, bucket_name, access_key, secret_key):
        """
        kirjoittaa .env tiedoston.
        """
        with open(".env", "w", encoding="utf-8") as file:
            file.write(
                f'AWS_ACCESS_KEY_ID="{access_key}"\nAWS_SECRET_ACCESS_KEY="{secret_key}"\nAWS_BUCKET_NAME="{bucket_name}"'
            )

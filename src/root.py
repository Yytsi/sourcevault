"""Moduuli joka toimii kaiken toiminnallisuuden juurena"""
from sqlite3 import OperationalError
import botocore.exceptions
import boto3.exceptions
from console_io import ConsoleIO


class Root:
    """
    Toiminnan ydin jota UI käskyttää.
    ...

    Attributes
    ----------
    my_sources : list
        Lista lähdeolioista.
    location : str
        Minne tallennetaan.

    Methods
    -------
    write_sources_bibtex():
        Kirjottaa lähdeoliot bibtexinä tallennuspaikkaan.
    add_source():
        Lisää annetun lähdeolion lähdelistaan.
    update_database():
        Päivittää tietokannan sisällön ohjelman sulkeutumisen yhteydessä
    remove_reference():
        Poistaa lähdeolion citation_keyn perusteella
    get_reference_by_key():
        Etsii lähdeolion citation_keyn perusteella
    """

    def __init__(
        self,
        data_handler,
        writer,
        cloud_data_handler,
        uses_database=True,
        io_handler=ConsoleIO(),
        sources=None,
        location="data.bib",
    ):
        """
        Luokan konstruktori.
        ...

        Parameters
        ----------
        sources : list
            Lista lähdeolioista.
        location : str
            Minne tallennetaan.
        """
        self.cloud_data_handler = cloud_data_handler
        self.data_handler = data_handler
        self.io_handler = io_handler
        self.writer = writer
        self.writer.location = location
        self.uses_database = uses_database
        if not sources:
            self.my_sources = []
        self.location = location

    def write_sources_bibtex(self):
        """
        Kirjottaa lähdeoliot bibtexinä tallennuspaikkaan.
        ...

        """
        self.writer.write_all_to_file(self.my_sources)

    def update_database(self):
        """
        1. Päivittää tietokannan sisällön ohjelman sulkeutumisen yhteydessä
        2. Tallentaa tietokannan pilvipalveluun
        ...


        """
        self.data_handler.update_database(self.my_sources)
        if self.uses_database:
            try:
                self.cloud_data_handler.upload_references()
            except boto3.exceptions.S3UploadFailedError:
                print("Unable to upload database to cloud")

    def read_sources_from_database(self):
        """
        1. Hakee tietokannan pilvipalvelusta
        2. Hakee tietokantaan tallennetut lähdeoliot
        ...

        """
        try:
            if self.uses_database:
                self.cloud_data_handler.get_references()
            self.my_sources = self.data_handler.get_all_references()
            return True
        except OperationalError:
            return False
        except botocore.exceptions.ClientError:
            print("Unable to import database from cloud")
            return False

    def add_source(self, ref):
        """
        Lisää annetun lähdeolion lähdelistaan.
        ...

        Parameters
        ----------
        source_info : Reference
            Lähdeolion tiedot.
        """
        while True:
            found_duplicate = False
            for existing_ref in self.my_sources:
                if existing_ref.citation_key == ref.citation_key:
                    # Duplicate, so modify <ref> to fit
                    ref.citation_key += ref.citation_key[-1]
                    found_duplicate = True
            if not found_duplicate:
                break

        self.my_sources.append(ref)

    def remove_reference(self, citation_key):
        """
        Poistaa lähdeolion citation_keyn perusteella
        ...

        Parameters
        ----------
        citation_key : str
            Lähdeolion citation_key.
        """
        for i, ref in enumerate(self.my_sources):
            if ref.citation_key == citation_key:
                self.my_sources.pop(i)
                return True
        return False

    def get_reference_by_key(self, citation_key):
        """
        Etsii lähdeolion citation_keyn perusteella
        ...

        Parameters
        ----------
        citation_key : str
            Lähdeolion citation_key.
        """
        for ref in self.my_sources:
            if ref.citation_key == citation_key:
                return ref
        return False

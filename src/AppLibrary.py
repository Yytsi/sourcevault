"""Kirjastot Root-olion luomista varten"""
import os
from root import Root
from app_ui import AppUI
from database_handler import Database
from writer import Writer
from stub_io import StubIO


class AppLibrary:
    """
    Robot Frameworkin käyttämä kirjasto.
    ...

    Attributes
    ----------
    _io : StubIO([])
        Käyttöliittymä stubi
    root: Root()
        Hyödynnetty root olio
    self.app: AppUI(self.root)
        käytetty UI

    Methods
    -------
    output_should_contain():
        Tarkistaa, tulostiko ohjelma tietyn outputin.
    input():
        Lisää komennon stubiin.
    run_application():
        Suorittaa komennot.
    clear():
        Tyhjentää tietokannan.
    get_string():
        Hakee viitteen tekstiversion.
    get_bibtex_location():
        Hakee bibtex-tiedoston sijainnin.
    """

    def __init__(self):
        """
        Luokan konstruktori.
        ...
        """
        self._io = StubIO([])

        self.root = Root(
            Database("robot_data.db"),
            Writer("robot_bibtex.bib"),
            cloud_data_handler=None,
            uses_database=False,
            io_handler=self._io,
        )
        self.app = AppUI(self.root)

    def output_should_contain(self, value):
        """
        Tarkistaa, tulostiko ohjelma tietyn outputin.
        ...

        Parameters
        ----------
        value : string
            Output
        """
        if not value in self._io.outputs:
            raise AssertionError(f'Output "{value}" is not in {str(self._io.outputs)}')

    def input(self, value):
        """
        Lisää komennon stubiin.
        ...

        Parameters
        ----------
        value : string
            Suoritettava komento.
        """
        self._io.inputs.append(value)

    def run_application(self):
        """
        Suorittaa komennot.
        ...
        """
        self.app.run_app()

    def clear(self):
        """
        Tyhjentää tietokannan.
        ...
        """
        self.root.data_handler.clear_database()
        keys=[source.citation_key for source in self.root.my_sources]
        for key in keys:
            self.root.remove_reference(key)

    def get_string(self, citation_key):
        """
        Hakee viitteen tekstiversion.
        ...

        Parameters
        ----------
        citation_key : string
            Viitteen avain.
        """
        return str(self.root.get_reference_by_key(citation_key))

    def get_bibtex_location(self):
        """
        Hakee bibtex-tiedoston sijainnin.
        ...
        """
        return f"Wrote to: {os.getcwd()}/{self.root.location} \n"

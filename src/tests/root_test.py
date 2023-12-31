import unittest
import botocore.exceptions
import boto3.exceptions
from root import Root
from writer import Writer
from database_handler import Database
from reference import Reference
from stub_io import StubIO
from sql_server import ServerHandler



class TestRoot(unittest.TestCase):
    def setUp(self):
        app_cloud_database = ServerHandler(
            "123", "12345", "test_database.db", "tietokanta.db", "sourcevaultbucket"
        )
        app_writer = Writer("test_bibtexdata.bib")
        db = Database("test_database.db")
        self.root = Root(
            db,
            app_writer,
            app_cloud_database,
            uses_database=False,
            io_handler=StubIO([]),
        )

    def test_can_add_source_to_database(self):
        ref = Reference(
            "book",
            "Martti08",
            tags=["good", "old"],
            year="2008",
            title="titled",
            author="Martti",
            publisher="publ",
        )

        self.root.add_source(ref)
        self.root.update_database()

        # Read sources from database
        self.root.read_sources_from_database()

        read_ref = self.root.my_sources[0]

        self.assertEqual(read_ref.reference_type, "book")
        self.assertEqual(read_ref.citation_key, "Martti08")
        self.assertEqual(str(read_ref.fields.get("year")), "2008")
        self.assertEqual(read_ref.fields.get("title"), "titled")
        self.assertEqual(read_ref.fields.get("author"), "Martti")
        self.assertEqual(read_ref.fields.get("publisher"), "publ")
        self.assertEqual(read_ref.tags[0], "good")
        self.assertEqual(read_ref.tags[1], "old")

    def test_cant_add_duplicate_source_to_database(self):
        ref = Reference(
            "book",
            "Martti08",
            tags=["good", "old"],
            year="2008",
            title="titled",
            author="Martti",
            publisher="publ",
        )

        ref2 = Reference(
            "book",
            "Martti08",
            tags=["good", "old"],
            year="2008",
            title="titled",
            author="Martti",
            publisher="publ",
        )

        self.root.add_source(ref)
        self.root.add_source(ref2)
        self.root.update_database()

        # Read sources from database
        self.root.read_sources_from_database()
        read_ref = self.root.my_sources[1]

        self.assertEqual(read_ref.reference_type, "book")
        self.assertEqual(read_ref.citation_key, "Martti088")
        self.assertEqual(str(read_ref.fields.get("year")), "2008")
        self.assertEqual(read_ref.fields.get("title"), "titled")
        self.assertEqual(read_ref.fields.get("author"), "Martti")
        self.assertEqual(read_ref.fields.get("publisher"), "publ")
        self.assertEqual(read_ref.tags[0], "good")
        self.assertEqual(read_ref.tags[1], "old")

    def test_search_reference_with_key_works(self):
        ref = Reference(
            "book",
            "Martti08",
            tags=["good", "old"],
            year="2008",
            title="titled",
            author="Martti",
            publisher="publ",
        )

        self.root.add_source(ref)
        valid_search = self.root.get_reference_by_key("Martti08")
        invalid_search = self.root.get_reference_by_key("Martti09")
        reference = self.root.my_sources[0]
        self.assertEqual(reference, valid_search)
        self.assertEqual(False, invalid_search)

    def test_cant_remove_non_existet_source_from_database(self):
        self.root.read_sources_from_database()
        # cant remove non-existent data
        self.assertEqual(self.root.remove_reference("Martti00"), False)

    def test_can_remove_source_from_database(self):
        self.root.read_sources_from_database()
        # Not empty, contains source added in previous test
        self.assertNotEqual(self.root.my_sources, [])
        self.root.remove_reference("Martti08")
        self.root.update_database()
        # Should now be empty
        self.root.read_sources_from_database()
        self.assertEqual(self.root.my_sources, [])

    def test_reading_from_cloud_fails_with_invalid_keys(self):
        self.root.uses_database = True
        self.root.read_sources_from_database()
        self.assertRaises(botocore.exceptions.ClientError)

    def test_uploading_to_cloud_fails_with_invalid_keys(self):
        self.root.uses_database = True
        self.root.update_database()
        self.assertRaises(boto3.exceptions.S3UploadFailedError)

"""Tests for extract module."""
#  pylint:disable=attribute-defined-outside-init import-error
import os
from unittest.mock import Mock, patch

from etl.extract.src.extract import (
    AuthorsExtract,
    BooksExtract,
    Extract,
    RecentChangesExtract,
)

SOURCE_PATH = "etl.extract.src.extract"


class TestExtractors:
    """Test class for extractors."""

    def test_init(self):
        """Test getting instance."""
        self.extractor = Extract(Mock())

    def test_books_extract_init(self):
        """Test getting instance."""
        self.extractor = BooksExtract(Mock())

    def test_authors_init(self):
        """Test getting instance."""
        self.extractor = AuthorsExtract(Mock())

    def test_recent_changes_init(self):
        """Test getting instance."""
        self.extractor = RecentChangesExtract(Mock())

    def test_download_data(self):
        """Test downloading data."""
        self.extractor = RecentChangesExtract(Mock())
        with patch(f"{SOURCE_PATH}.json"):
            self.extractor.download_data()

    def test_extract(self):
        """Test extract."""
        self.extractor = RecentChangesExtract(Mock())
        with patch(f"{SOURCE_PATH}.json"):
            self.extractor.extract()

    def test_save_to_csv_no_header(self):
        """Test saving to csv."""
        with open("foo", "w") as test_file:
            test_file.write("bar")
        self.extractor = Extract(Mock())
        self.extractor.FIELD_NAMES = ["foo"]
        self.extractor.file_name = "foo"
        self.extractor.data = {"foo": "bar"}
        try:
            self.extractor.save_to_csv()
        finally:
            os.remove(self.extractor.file_name)

    def test_save_to_csv_with_header(self):
        """Test saving to csv."""
        self.extractor = Extract(Mock())
        self.extractor.FIELD_NAMES = ["foo"]
        self.extractor.file_name = "foo"
        self.extractor.data = {"foo": "bar"}
        try:
            self.extractor.save_to_csv()
        finally:
            os.remove("foo.csv")

    def test_save_to_csv_no_headers(self):
        """Test saving to csv."""
        self.extractor = Extract(Mock())
        self.extractor.FIELD_NAMES = ["foo"]
        self.extractor.file_name = "foo"
        self.extractor.data = {}
        try:
            self.extractor.save_to_csv()
        finally:
            os.remove("foo.csv")

    def test_save_recent_changes_to_csv(self):
        """Test saving to csv."""
        with open("foo", "w") as test_file:
            test_file.write("bar")
        self.extractor = RecentChangesExtract(Mock())
        self.extractor.FIELD_NAMES = ["foo"]
        self.extractor.file_name = "foo"
        self.extractor.data = [{"foo": "bar"}]
        try:
            self.extractor.save_to_csv()
        finally:
            os.remove("foo.csv")
            os.remove("foo")

    def test_generate_url(self):
        """Test generate url."""
        self.extractor = RecentChangesExtract(Mock())
        self.extractor.for_date_key = "2021/06/24"
        self.extractor.generate_url()

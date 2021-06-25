"""Multi purpose extracting module."""
#  pylint: disable=no-member too-many-arguments
import csv
import json
import os
from collections import OrderedDict
from datetime import datetime
from typing import Any, List
from urllib.parse import urlencode

from urllib3 import PoolManager

BASE_URL = "http://openlibrary.org"
RECENT_CHANGES = "recentchanges"
BOOKS = "books"
AUTHORS = "authors"
JSON = ".json"
DATA_DIR = "data"
LIMIT = 10000
CSV = ".csv"


class Extract:
    """Generic data extractor."""

    NOW = datetime.utcnow()
    FIELD_NAME: List[str] = []

    def __init__(
        self,
        http_client: PoolManager,
        url: str = None,
        file_name: str = None,
        for_date_key: str = "",
        extract_type: str = "",
    ):
        """Setup the extractor."""
        self.http = http_client
        self.data: Any = [None]
        self.url = url
        self.file_name = file_name
        self.for_date_key = for_date_key
        self.extract_type = extract_type

    def download_data(self):
        """Download data from the given URL."""
        self.data = json.loads(self.http.request("GET", self.url).data)

    def extract(self):
        """Fetch the data and save it to a CSV."""
        self.generate_url()
        self.generate_file_name()
        self.download_data()
        self.save_to_csv()

    def save_to_csv(self):
        """Export data to CSV file."""
        write_header = not os.path.exists(self.file_name + CSV)
        with open(self.file_name + CSV, "a") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self.FIELD_NAMES)
            if write_header:
                csv_writer.writeheader()
            for field in self.FIELD_NAMES:
                if not self.data.get(field):
                    self.data[field] = ""
            csv_writer.writerow(self.data)

    def generate_url(self):
        """Provide a URL for fetching data."""
        query_string = OrderedDict(limit=LIMIT)
        if self.for_date_key:
            self.for_date_key = "/" + self.for_date_key
        if not self.url:
            self.url = (
                f"{BASE_URL}/{self.extract_type}{self.for_date_key}"
                f"{JSON}?{urlencode(query_string)}"
            )

    def generate_file_name(self):
        """Provide a file name to save data to CSV."""
        if not self.file_name:
            self.file_name = f"{DATA_DIR}/{self.extract_type}-" f"{self.NOW}"


class RecentChangesExtract(Extract):
    """Extract from Recent Changes API."""

    def save_to_csv(self):
        """Export data to CSV file."""
        write_header = not os.path.exists(self.file_name + CSV)
        with open(self.file_name + CSV, "a") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self.data[0].keys())
            if write_header:
                csv_writer.writeheader()
            csv_writer.writerows(self.data)


class AuthorsExtract(Extract):
    """Extract from Authors API."""

    FIELD_NAMES = [
        "wikipedia",
        "key",
        "remote_ids",
        "created",
        "birth_date",
        "name",
        "latest_revision",
        "last_modified",
        "alternate_names",
        "type",
        "photos",
        "revision",
        "personal_name",
        "death_date",
        "source_records",
        "id",
        "bio",
        "links",
        "title",
        "data",
        "date",
        "fuller_name",
        "location",
    ]


class BooksExtract(Extract):
    """Extract from Books API."""

    FIELD_NAMES = [
        "subtitle",
        "authors",
        "title",
        "publishers",
        "number_of_pages",
        "physical_format",
        "notes",
        "works",
        "publish_date",
        "isbn_10",
        "covers",
        "full_title",
        "isbn_13",
        "last_modified",
        "created",
        "type",
        "key",
        "latest_revision",
        "revision",
        "source_records",
        "name",
        "id",
        "publish_places",
        "identifiers",
        "pagination",
        "classifications",
        "copyright_date",
        "table_of_contents",
        "contributors",
        "edition_name",
        "oclc_numbers",
        "languages",
        "other_titles",
        "subjects",
        "links",
        "subject_places",
        "description",
        "subject_times",
        "excerpts",
        "subject_people",
        "series",
        "lc_classifications",
        "first_publish_date",
        "dewey_number",
        "physical_dimensions",
        "first_sentence",
        "weight",
        "translation_of",
        "by_statement",
        "translated_from",
        "dewey_decimal_class",
        "ocaid",
        "location",
        "publish_country",
        "personal_name",
    ]


if __name__ == "__main__":
    http = PoolManager()
    recent_changes = RecentChangesExtract(http, extract_type=RECENT_CHANGES)
    recent_changes.extract()
    for row in recent_changes.data:
        if row["kind"] == "add-book":
            for change in row["changes"]:
                book = BooksExtract(
                    http,
                    extract_type=BOOKS,
                    url=BASE_URL + change["key"] + JSON,
                )
                book.extract()
                if book.data.get("authors"):
                    for author in book.data["authors"]:
                        AuthorsExtract(
                            http,
                            extract_type=AUTHORS,
                            url=BASE_URL + author.get("author", author)["key"] + JSON,
                        ).extract()

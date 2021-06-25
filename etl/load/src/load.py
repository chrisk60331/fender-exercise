"""Multi purpose loading module."""
#  pylint:disable=redefined-outer-name attribute-defined-outside-init too-few-public-methods import-error
import csv
import sqlite3

from etl.extract.src.extract import AuthorsExtract, BooksExtract

DB_CONFIG = open("db_config", "r").read()


class DBLoader:
    """Generic database loader."""

    def __init__(self, connection, config):
        """Setup the dbloader."""
        self.connection = connection
        for table_name, (file_name, field_names) in config.items():
            self.load_table(table_name, file_name, field_names)

    def load_table(self, table_name, file_name, field_names):
        """Load a table."""
        cur = self.connection.cursor()

        with open(file_name, "r") as data_file:
            next(csv.reader(data_file))
            cur.executemany(
                f"""INSERT INTO {table_name} ({", ".join(field_names)}) """
                f"""VALUES ({'?'+ ', ?' * (len(field_names)-1)})""",
                csv.reader(data_file),
            )
        self.connection.commit()


if __name__ == "__main__":  # pragma: no-cover
    con = sqlite3.connect(DB_CONFIG)
    load_config = {
        "books": (
            "datalake/books.csv",
            BooksExtract.FIELD_NAMES,
        ),
        "authors": (
            "datalake/authors.csv",
            AuthorsExtract.FIELD_NAMES,
        ),
        "book_and_authors": "datalake/book_and_authors.csv",
    }
    DBLoader(con, load_config)
    con.close()

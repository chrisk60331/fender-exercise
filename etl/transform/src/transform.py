"""Multi purpose transformer module."""
# pylint: disable=unsupported-assignment-operation unsubscriptable-object arguments-differ inconsistent-return-statements
import json
from typing import Tuple

import pandas


class Transformer:
    """Multi purpose transformer."""

    def __init__(
        self,
        in_file: str = None,
        out_file: str = None,
        transformations: dict = None,
    ):
        """Setup the transformer."""
        self.in_file = in_file
        self.dataframe = self.load_file()
        self.out_file = out_file
        if transformations:
            for transform, targets in transformations.items():
                method = getattr(self, transform)
                if callable(method):
                    for target in targets:
                        method(target)
        if in_file and out_file:
            self.export()

    def export(self):
        """Save to csv."""
        self.dataframe.to_csv(self.out_file)

    def unpack(self, column_name: str):
        """Unpack nested structures."""
        self.dataframe[column_name] = (
            self.dataframe[column_name].dropna().apply(clean_json)
        )

    def rename(self, column_names: Tuple[str, str]):
        """Rename a column."""
        column_name, new_column_name = column_names
        self.dataframe.rename(columns={column_name: new_column_name})

    def load_file(self):
        """Pass-through for loading from data frame."""
        return self.in_file


class CSVTransformer(Transformer):
    """Load from CSV and transform."""

    def load_file(self):
        """Load one csv file."""
        if self.in_file:
            return pandas.read_csv(self.in_file)


def clean_json(column):
    """Flatten nested data."""
    data = column.replace("'", '"')
    try:
        data = json.loads(data)[0]
    except json.decoder.JSONDecodeError:
        return data
    return data.get("type", data).get("key")


if __name__ == "__main__":
    transformation = {
        "rename": [
            ("authors_key", "authors"),
            ("books_key", "key"),
        ],
        "unpack": ["authors_key", "books_key"],
    }
    books = CSVTransformer(
        in_file="data/books-2021-06-24 13:00:32.671568.csv",
        out_file="datalake/books.csv",
        transformations=transformation,
    )
    authors_and_books = books.dataframe[["authors_key", "books_key"]]
    Transformer(
        in_file=authors_and_books,
        out_file="datalake/authors_and_books.csv",
    )
    CSVTransformer(
        in_file="data/authors-2021-06-24 13:00:32.671568.csv",
        out_file="datalake/authors.csv",
        transformations={
            "rename": [
                ("authors_key", "key"),
            ],
            "unpack": ["authors_key"],
        },
    )

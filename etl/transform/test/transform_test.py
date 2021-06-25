"""Tests fir transform module."""
#  pylint:disable=redefined-outer-name attribute-defined-outside-init too-few-public-methods import-error implicit-str-concat

import os

import pytest

from etl.transform.src.transform import CSVTransformer, Transformer, clean_json


@pytest.fixture
def test_file():
    """Local file fixture."""
    try:
        with open(TestTransformer.test_file_name, "w") as test_file:
            test_file.write("foo")
        yield TestTransformer.test_file_name
    finally:
        os.remove(TestTransformer.test_file_name)


class TestTransformer:
    """Test clase for transformer."""

    test_file_name = "test_file"

    def test_transformer_out_file_no_in_file(self):
        """Test what happens when no in file is supplied."""
        self.transformer = Transformer(out_file="foo")


class TestCSVTransformer:
    """Tests for csv transformer."""

    def test_transformer_out_file(self):
        """Make sure we can create instance."""
        self.csv_transformer = CSVTransformer(out_file="foo")

    def test_transformer_out_file_with_in_file(self, test_file):
        """Make sure we can create instance with in file."""
        self.transformer = CSVTransformer(in_file=test_file, out_file="foo")

    def test_transformer_unpack(self, test_file):
        """Make sure we can save to a file."""
        self.transformer = CSVTransformer(
            in_file=test_file, out_file="foo", transformations={"unpack": ["foo"]}
        )

    def test_transformer_rename(self, test_file):
        """Make sure we can rename columns."""
        try:
            self.transformer = CSVTransformer(
                in_file=test_file,
                out_file="foo",
                transformations={"rename": [("foo", "bar")]},
            )
        finally:
            os.remove("foo")


@pytest.mark.parametrize(
    "expected, test_input",
    [
        ("foo", str([{"type": {"key": "foo"}}])),
        ('{"foobar"}', str({"foo" "bar"})),
    ],
)
def test_clean_json(expected, test_input):
    """Test to make sure we get expected output."""
    actual = clean_json(test_input)

    assert expected == actual

"""Tests for the load module."""
#  pylint:disable=redefined-outer-name attribute-defined-outside-init too-few-public-methods import-error
import os
from unittest.mock import Mock

from etl.load.src.load import DBLoader


class TestDBLoader:
    """Test class for DBLoader."""

    def test_init(self):
        """Test creating an instance."""
        self.db_loader = DBLoader(Mock(), {})

    def test_load_table(self):
        """Test loading a table."""
        mock_con = Mock()
        with open("test_file", "w") as test_file:
            test_file.writelines(["bing", "zoop"])
        try:
            self.db_loader = DBLoader(
                connection=mock_con, config={"foo": ("test_file", ["baz"])}
            )
        finally:
            os.remove("test_file")

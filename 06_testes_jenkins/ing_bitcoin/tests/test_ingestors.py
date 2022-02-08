from cmath import exp
import datetime
from unittest import mock
from unittest.mock import mock_open, patch

import pytest
from mercadobitcoinapi.ingestors import DataIngestor
from mercadobitcoinapi.writers import DataWriter


@pytest.fixture
@patch("mercadobitcoinapi.ingestors.DataIngestor.__abstractmethods__", set())
def data_ingestor_fixture():
    return DataIngestor(
        writer=DataWriter,
        coins=["TEST", "HOW"],
        default_start_date=datetime.date(2021, 6, 21),
    )


@patch("mercadobitcoinapi.ingestors.DataIngestor.__abstractmethods__", set())
class TestIngestors:
    def test_checkpoint_filename(self, data_ingestor_fixture):
        actual = data_ingestor_fixture._checkpoint_filename

        expected = "DataIngestor.checkpoint"

        assert actual == expected

    def test_load_checkpoint_no_checkpoint(self, data_ingestor_fixture):
        actual = data_ingestor_fixture._load_checkpoint()

        expected = datetime.date(2021, 6, 21)

        assert actual == expected

    @patch("builtins.open", new_callable=mock_open, read_data="2021-06-25")
    def test_load_checkpoint_with_checkpoint(self, mock, data_ingestor_fixture):
        actual = data_ingestor_fixture._load_checkpoint()

        expected = datetime.date(2021, 6, 25)

        assert actual == expected

    @patch(
        "mercadobitcoinapi.ingestors.DataIngestor._write_checkpoint", return_value=None
    )
    def test_load_checkpoint_updated(self, mock, data_ingestor_fixture):
        data_ingestor_fixture._update_checkpoint(value=datetime.date(2019, 1, 1))
        actual = data_ingestor_fixture._checkpoint
        expected = datetime.date(2019, 1, 1)
        assert actual == expected

    @patch("builtins.open", new_callable=mock_open, read_data="2021-06-25")
    @patch(
        "mercadobitcoinapi.ingestors.DataIngestor._checkpoint_filename",
        return_value="foobar.checkpoint",
    )
    def test_write_checkpoint(
        self, mock_checkpoint_filename, mock_open_file, data_ingestor_fixture
    ):
        data_ingestor_fixture._write_checkpoint()
        mock_open_file.assert_called_with(mock_checkpoint_filename, "w")

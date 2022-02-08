import datetime
from unittest.mock import patch
from urllib.request import Request
import pytest
import requests

from mercadobitcoinapi.apis import DaySummaryApi, MercadoBitcoinApi, TradesApi


class TestDaySummaryApi:
    @pytest.mark.parametrize(
        "coin, date, expected",
        [
            (
                "BTC",
                datetime.date(2021, 6, 21),
                "https://www.mercadobitcoin.net/api/BTC/day-summary/2021/6/21",
            ),
            (
                "ETH",
                datetime.date(2022, 1, 1),
                "https://www.mercadobitcoin.net/api/ETH/day-summary/2022/1/1",
            ),
        ],
    )
    def test_get_endpoint(self, coin, date, expected):
        api = DaySummaryApi(coin=coin)
        actual = api._get_endpoint(date=date)
        assert actual == expected


class TestTradesApi:
    def test_get_endpoint_date_from_greater_than_date_to(self):
        with pytest.raises(RuntimeError):
            TradesApi(coin="TEST")._get_endpoint(
                date_from=datetime.datetime(2019, 6, 6),
                date_to=datetime.datetime(2019, 1, 1),
            )

    @pytest.mark.parametrize(
        "coin, date_from, date_to, expected",
        [
            (
                "TEST",
                datetime.datetime(2019, 1, 1),
                datetime.datetime(2019, 1, 2),
                "https://www.mercadobitcoin.net/api/TEST/trades/1546308000/1546394400",
            ),
            (
                "TEST",
                datetime.datetime(2019, 1, 1),
                datetime.datetime(2021, 6, 12),
                "https://www.mercadobitcoin.net/api/TEST/trades/1546308000/1623466800",
            ),
            ("TEST", None, None, "https://www.mercadobitcoin.net/api/TEST/trades"),
            (
                "TEST",
                None,
                datetime.datetime(2021, 6, 12),
                "https://www.mercadobitcoin.net/api/TEST/trades",
            ),
            (
                "TEST",
                datetime.datetime(2019, 1, 1),
                None,
                "https://www.mercadobitcoin.net/api/TEST/trades/1546308000",
            ),
        ],
    )
    def test_get_endpoint(self, coin, date_from, date_to, expected):
        api = TradesApi(coin=coin)
        actual = api._get_endpoint(date_from=date_from, date_to=date_to)
        assert actual == expected

    @pytest.mark.parametrize(
        "date, expected",
        [
            (datetime.datetime(2019, 1, 1), 1546308000),
            (datetime.datetime(2019, 1, 2), 1546394400),
            (datetime.datetime(2021, 6, 12), 1623466800),
        ],
    )
    def test_get_unix_epoch(self, date, expected):
        api = TradesApi(coin="TEST")
        actual = api._get_unix_epoch(date)
        assert actual == expected


@pytest.fixture
@patch("mercadobitcoinapi.apis.MercadoBitcoinApi.__abstractmethods__", set())
def fixture_mercadobitcoin_api():
    return MercadoBitcoinApi(coin="TESTE")


def mocked_requests_get(*args, **kwargs):
    class MockResponse(requests.Response):
        def __init__(self, json_data, status_code) -> None:
            super().__init__()
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def raise_for_status(self) -> None:
            if self.status_code != 200:
                raise Exception

    if args[0] == "valid_endpoint":
        return MockResponse(json_data={"foo": "bar"}, status_code=200)
    else:
        return MockResponse(json_data=None, status_code=404)


@patch("mercadobitcoinapi.apis.MercadoBitcoinApi.__abstractmethods__", set())
class TestMercadoBitcoinApi:
    @patch("requests.get")
    @patch(
        "mercadobitcoinapi.apis.MercadoBitcoinApi._get_endpoint",
        return_value="valid_endpoint",
    )
    def test_get_data_requests_is_called(
        self, mock_get_endpoint, mock_requests_get, fixture_mercadobitcoin_api
    ):
        fixture_mercadobitcoin_api.get_data()
        mock_requests_get("valid_endpoint")

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch(
        "mercadobitcoinapi.apis.MercadoBitcoinApi._get_endpoint",
        return_value="valid_endpoint",
    )
    def test_get_data_with_valid_endpoint(
        self, mock_get_endpoint, mock_requests_get, fixture_mercadobitcoin_api
    ):
        actual = fixture_mercadobitcoin_api.get_data()
        expected = {"foo": "bar"}
        assert actual == expected

    @patch("requests.get", side_effect=mocked_requests_get)
    @patch(
        "mercadobitcoinapi.apis.MercadoBitcoinApi._get_endpoint",
        return_value="invalid_endpoint",
    )
    def test_get_data_with_valid_endpoint(
        self, mock_get_endpoint, mock_requests_get, fixture_mercadobitcoin_api
    ):
        with pytest.raises(Exception):
            fixture_mercadobitcoin_api.get_data()

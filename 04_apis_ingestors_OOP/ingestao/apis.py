from abc import ABC, abstractclassmethod
import datetime
from typing import List
import requests
import logging
import ratelimit
import backoff


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MercadoBitcoinApi(ABC):

    def __init__(self, coin: str) -> None:
        self.coin = coin
        self.base_endpoint = 'https://www.mercadobitcoin.net/api'

    @abstractclassmethod
    def _getendpoint(self, **kwargs) -> str:
        pass

    @backoff.on_exception(backoff.expo, ratelimit.exception.RateLimitException, max_tries=10)
    @ratelimit.limits(calls=29, period=30)
    @backoff.on_exception(backoff.expo, requests.exceptions.HTTPError, max_tries=10)
    def get_data(self, **kwargs) -> dict:
        endpoint = self._getendpoint(**kwargs)
        logger.info(f"Getting data from endpoint: {endpoint}")
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()

class DaySummaryApi(MercadoBitcoinApi):

    type = 'day-summary'

    def _getendpoint(self, date: datetime.date) -> str:
        return f"{self.base_endpoint}/{self.coin}/{self.type}/{date.year}/{date.month}/{date.day}/"


class TradesApi(MercadoBitcoinApi):

    type = 'trades'

    def _get_unix_epoch(self, date:datetime.date):
        return int(date.timestamp())

    def _getendpoint(self, date_from: datetime.date = None, date_to: datetime.date = None) -> str:

        if date_from and not date_to:
            unix_date_from = self._get_unix_epoch(date_from)
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}"

        elif date_from and date_to:
            unix_date_from = self._get_unix_epoch(date_from)
            unix_date_to = self._get_unix_epoch(date_to)
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}/{unix_date_to}"
        
        else:
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}"

        return endpoint
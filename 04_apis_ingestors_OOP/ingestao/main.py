import datetime
from typing import List
from schedule import repeat, every, run_pending
import time

from ingestors import DaySummaryIngestor
from writers import DataWriter



if __name__ == "__main__":
    day_summary_ingestor = DaySummaryIngestor(
        writer=DataWriter,
         coins = ['BTC','ETH','LTC'],
          default_startdate=datetime.date(2021,6,1)
          )

    @repeat(every(1).seconds)
    def job():
        day_summary_ingestor.ingest()

    #every(1).seconds.do(job())

    while True:
        run_pending()
        time.sleep(0.5)

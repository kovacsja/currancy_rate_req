import requests
import sqlite3
import logging
from datetime import datetime, timedelta


def create_db():
    conn = sqlite3.connect("rates.sqlite")
    curr = conn.cursor()

    curr.execute(
        """
        CREATE TABLE IF NOT EXISTS rates (
            Exc_date date, 
            Currency text,
            Exc_rate real, 
            primary key (Exc_date, Currency)
        )
        """
    )
    conn.commit()

    curr.close()
    conn.close()


def get_rates():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    log_stream = logging.StreamHandler()
    logger.addHandler(log_stream)
    log_stream.setLevel(logging.INFO)

    conn = sqlite3.connect("rates.sqlite")
    curr = conn.cursor()
    base: str = "EUR,USD,CZK,HUF"
    date_range = 90
    today = datetime.today().date()
    dates = [today]
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }
    acc_key: str = "3fabb4865832bd33fda308d1cfbbe9fd"

    maxdate = curr.execute("select max(exc_date) from rates").fetchone()

    if maxdate[0] != (None,):
        while maxdate[0] < today.strftime("%Y-%m-%d"):
            today = today - timedelta(days=1)
            dates.append(today)
    else:
        for i in range(date_range):
            today = today - timedelta(days=1)
            dates.append(today)

    if len(dates) != 1 and maxdate != today:
        for d in dates:
            date_str: str = datetime.strftime(d, "%Y-%m-%d")
            logger.info(date_str)
            url = f"http://api.exchangeratesapi.io/v1/{date_str}?access_key={acc_key}&symbols={base}"
            response = requests.get(url=url, headers=headers, timeout=25)
            data = response.json()

            for i in data["rates"]:
                curr.executemany(
                    "insert into rates values (?, ?, ?)",
                    [(date_str, i, data["rates"][i])],
                )
                conn.commit()

    curr.close()
    conn.close()


def main():
    get_rates()


if __name__ == "__main__":
    main()

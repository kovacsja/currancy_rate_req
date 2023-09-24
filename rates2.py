import requests
import pandas as pd
from datetime import datetime, timedelta

# import streamlit as st

# here https://api.exchangerate.host/ is the host
# timeseries is one of the stamps for data type
# timeseries fetch all data set in between the mentioned dates

base: list[str] = ["EUR", "USD"]
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = datetime.strftime(datetime.now() - timedelta(days=90), "%Y-%m-%d")
out_curr: str = "HUF"
rates = []
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
}

for bcurr in base:
    url = f"https://api.exchangerate.host/timeseries?base={bcurr}&start_date={start_date}&end_date={end_date}&symbols={out_curr}"
    response = requests.get(url, headers=headers, timeout=5)

    data = response.json()

    for i, j in data["rates"].items():
        rates.append([i, bcurr, j[out_curr]])

df = pd.DataFrame(rates)

df.columns = ["date", "curr", "rate"]

print(df)

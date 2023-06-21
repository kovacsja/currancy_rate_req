import requests
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

# import streamlit as st

# here https://api.exchangerate.host/ is the host
# timeseries is one of the stamps for data type
# timeseries fetch all data set in between the mentioned dates

base: list[str] = ["EUR", "USD"]
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = datetime.strftime(datetime.now() - timedelta(days=90), "%Y-%m-%d")
out_curr: str = "HUF"
rates = []

for bcurr in base:
    url = f"https://api.exchangerate.host/timeseries?base={bcurr}&start_date={start_date}&end_date={end_date}&symbols={out_curr}"
    response = requests.get(url, timeout=5)

    data = response.json()

    for i, j in data["rates"].items():
        rates.append([i, bcurr, j[out_curr]])

df = pd.DataFrame(rates)

df.columns = ["date", "curr", "rate"]

print(df)

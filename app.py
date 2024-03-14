import requests
import json
from datetime import datetime, timedelta
from binance.client import Client
import os
from configparser import ConfigParser
from forex_python.converter import CurrencyRates

# Load configuration file
config = ConfigParser()
config.read('config.ini')

# Binance API Key and Secret
api_key = os.environ.get(config.get('DEAL_RUN_VALUATION', 'APIKey'))
api_secret = os.environ.get(config.get('DEAL_RUN_VALUATION', 'APISecret'))
binance_client = Client(api_key, api_secret)

def get_binance_price(keyword, datetime_str):
    symbol_map = {
        "Bitcoin": "BTCUSDT",
        "Ethereum": "ETHUSDT"
    }
    symbol = symbol_map.get(keyword)
    if not symbol:
        raise ValueError(f"Invalid cryptocurrency: {keyword}")

    specific_time = datetime.fromisoformat(datetime_str)
    specific_time_ms = int(specific_time.timestamp() * 1000)  # Convert to milliseconds

    klines = binance_client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, str(specific_time_ms), str(specific_time_ms+60000))

    if klines:
        close_price = klines[0][4]
        return float(close_price)
    else:
        return "No data available for the specified time"
    
def api_valuate_deals(keyword, date, price):
    api_url = "http://127.0.0.1:5000/Valuate_Deals"
    data = json.dumps({"keyword": keyword, "date": date, "price": price})
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(api_url, data=data, headers=headers)
        if response.status_code == 200:
            print("Update successful:", response.json())
        else:
            print(f"Error during update: {response.status_code}", response.json())
    except requests.RequestException as e:
        print(f"Error making request to the API: {e}")

def run_valuation(keyword):
    start_date = datetime(year=2023, month=1, day=2)
    end_date = datetime(year=2024, month=3, day=13)
    delta = timedelta(days=1)
    current_date = start_date

    while current_date <= end_date:
        print(f"Valuating {keyword} for {current_date.strftime('%d-%m-%Y')}...")
        datetime_str = current_date.strftime('%Y-%m-%dT00:00:00')
        price = get_binance_price(keyword, datetime_str)
        api_valuate_deals(keyword, current_date.strftime("%d-%m-%Y"), price)
        print(keyword, current_date.strftime("%d-%m-%Y"), price)
        current_date += delta

run_valuation("Bitcoin")
run_valuation("Ethereum")
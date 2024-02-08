import requests
import json
from datetime import datetime, timedelta, timezone

def get_bitcoin_price_date(date):
    date_formatted = datetime.datetime.strptime(date, "%d-%m-%Y").strftime("%d-%m-%Y")
    url = f"https://api.coingecko.com/api/v3/coins/bitcoin/history?date={date_formatted}&localization=false"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["market_data"]["current_price"]["usd"]
    except requests.RequestException as e:
        return None

def api_valuate_deals(keyword, date, price):
    api_url = "http://127.0.0.1:5000/Valuate_Deals"
    data = json.dumps({"date": date, "keyword": keyword, "date": date, "price": price}) 
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(api_url, data=data, headers=headers)
        if response.status_code == 200:
            print("Update successful:", response.json())
        else:
            print("Error during update:", response.json())
    except requests.RequestException as e:
        print(f"Error making request to the API: {e}")

def valuate_bitcoin(date):
    keyword = "Bitcoin"
    price = get_bitcoin_price_date(date)
    api_valuate_deals(keyword, date, price)

#date = "14-04-2023"
#valuate_bitcoin(date)
    
day = 0
price = 28000
while day < 30:
    keyword = "Bitcoin"
    if day < 5:
        price = price *1.05
    if day >= 5 and day < 10:
        price = price *0.95
    if day >= 10 and day < 15:
        price = price *1.05
    if day >= 15 and day < 20:
        price = price *0.95
    if day >= 20 and day < 25:
        price = price *1.05
    if day >= 25 and day < 30:
        price = price *0.90

    day = day+1
    if day < 10:
        day_string = f"0{day}"
    else: 
        day_string = f"{day}"
    date = day_string + "-01-2023"
    api_valuate_deals(keyword, date, price)
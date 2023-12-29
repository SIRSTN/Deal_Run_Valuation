import requests
import json

def valuate_deals(api_url, date, keyword):
    data = json.dumps({"date": date, "keyword": keyword}) 
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(api_url, data=data, headers=headers)
        if response.status_code == 200:
            print("Update successful:", response.json())
        else:
            print("Error during update:", response.json())
    except requests.RequestException as e:
        print(f"Error making request to the API: {e}")

api_url = "http://127.0.0.1:5000/Valuate_Deals"
#valuation_date = "14-04-2023"
#valuation_date = "14-06-2023"
#valuation_date = "22-07-2023"
#valuation_date = "11-09-2023"
keyword = "Bitcoin"
valuate_deals(api_url, valuation_date, keyword)

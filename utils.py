import os
import requests


# Get statistics from API
def get_country_statistics(country):
    url = f"https://covid-19-tracking.p.rapidapi.com/v1/{country}"
    headers = {
        'x-rapidapi-key': os.getenv('RAPIDAPI_KEY'),
        'x-rapidapi-host': os.getenv('RAPIDAPI_HOST')
    }
    response = requests.request("GET", url, headers=headers)

    return response.json()

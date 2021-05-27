import requests
import settings


# Gets statistics from API
def get_country_statistics(country):
    url = f"https://covid-19-tracking.p.rapidapi.com/v1/{country}"
    headers = settings.HEADERS
    response = requests.request("GET", url, headers=headers)

    return response.json()

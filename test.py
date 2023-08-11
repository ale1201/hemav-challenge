import requests
from urllib.request import urlretrieve

api_key = 'jHz62lX9FUdeUOmJUlZmI1PnhpgRKCCuInhsfB7H'

import requests

url = "https://any-anime.p.rapidapi.com/anime/img"

headers = {
	"X-RapidAPI-Key": "SIGN-UP-FOR-KEY",
	"X-RapidAPI-Host": "any-anime.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

print(response.json())
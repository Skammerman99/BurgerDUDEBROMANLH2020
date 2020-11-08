import requests
from config import RG_API_KEY

# Basic Riot API Query

def getJSON():
    summoner_name = "thekillakela"
    url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": RG_API_KEY
    }

    response = requests.request("GET", url+summoner_name, headers=headers)
    print(response.json())

getJSON()

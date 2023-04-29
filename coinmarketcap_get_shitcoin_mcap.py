import os
from requests import Session
from dotenv import load_dotenv, find_dotenv
import json

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

COINMARKETCAP_API_KEY = os.environ.get("COINMARKETCAP_API_KEY")

def coinmarketcap_get_shitcoin_mcap(shitcoin):
    if not COINMARKETCAP_API_KEY:
        print("MISSING COINMARKETCAP API KEY. SET COINMARKETCAP_API_KEY in .env")
        exit()
    
    headers = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY}

    session = Session()
    session.headers.update(headers)
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = { 'symbol': shitcoin, 'convert': 'USD' } # API parameters to pass in for retrieving specific cryptocurrency data

    response = session.get(url, params=parameters)
    shitcoin_mcap = json.loads(response.text)['data'][shitcoin]['quote']['USD']['market_cap']
    return shitcoin, shitcoin_mcap
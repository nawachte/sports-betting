import requests
from bs4 import BeautifulSoup
from pprint import pprint

def get_page_data(url):
    # Set up headers (optional)
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    # Fetch the JSON data from the API
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # return response
        content_type = response.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            # It's JSON content
            data = response.json()
            return data
        elif 'text/html' in content_type:
            # It's HTML content
            html_content = response.text
            return html_content
        else:
            print("Error: bad content type |",content_type)
    else:
        print(f"Failed to retrieve the data. Status code: {response.status_code}")
        print(f"Resonpse content: {response.text}")
        exit()

def get_moneylines(sport,api_key):
    API_KEY = api_key
    SPORT = sport
    REGIONS = "us"
    MARKETS = "h2h"
    ODDS_FORMAT = "american"
    BASE_URL = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds"

    params = {
        "apiKey": API_KEY,
        "regions": REGIONS,
        "markets": MARKETS,
        "oddsFormat": ODDS_FORMAT
    }

    response = requests.get(BASE_URL, params=params)

    def shorten_team_name(team_name: str) -> str:
        # Split by space and take the last word. Example: "New York Giants" -> "Giants"
        return team_name.split()[-1]
    
    moneylines = {}

    if response.status_code == 200:
        data = response.json()

        # We are looking specifically for DraftKings, FanDuel, and BetMGM
        target_books = ["draftkings", "fanduel", "betmgm"]
        book_name_map = {
            "draftkings": "DraftKings",
            "fanduel": "FanDuel",
            "betmgm": "BetMGM"
        }

        for event in data:
            away_team_full = event.get("away_team")
            home_team_full = event.get("home_team")

            # Shorten the team names
            away_team_short = shorten_team_name(away_team_full)
            home_team_short = shorten_team_name(home_team_full)

            # Initialize a structure to hold odds from target books
            # We'll store as a dict temporarily: { 'DraftKings': (odds_away, odds_home), ... }
            event_odds = {}

            for bookmaker in event.get("bookmakers", []):
                key = bookmaker.get("key")
                if key in target_books:
                    # Find the h2h market within this bookmaker
                    for market in bookmaker.get("markets", []):
                        if market.get("key") == "h2h":
                            outcomes = market.get("outcomes", [])
                            # outcomes typically look like: [{"name": "Team A", "price": -110}, {"name": "Team B", "price": -112}]
                            # We need to match the outcome to the away/home team to keep consistency in ordering.
                            # The API returns team names in full format, so we should match them directly.
                            away_price = None
                            home_price = None
                            for outcome in outcomes:
                                if outcome["name"] == away_team_full:
                                    away_price = outcome["price"]
                                elif outcome["name"] == home_team_full:
                                    home_price = outcome["price"]
                            
                            # Only add if we got both away and home prices
                            if away_price is not None and home_price is not None:
                                event_odds[book_name_map[key]] = [away_price, home_price]

            # Only add to dictionary if we have at least one bookmaker's odds
            if event_odds:
                # Convert dictionary to a list of lists in the desired format
                # The order is away_team_short, home_team_short for the key
                # Each value entry: [BookName, away_odds, home_odds]
                value_list = []
                for bk, prices in event_odds.items():
                    value_list.append([bk, prices[0], prices[1]])

                moneylines[(away_team_short, home_team_short)] = value_list
    
    return moneylines

def get_NFL_moneylines():
    return get_moneylines("americanfootball_nfl","#######################")

def get_NBA_moneylines():
    return get_moneylines("basketball_nba","#######################")

        

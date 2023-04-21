import json
from datetime import datetime

import requests
from rich.console import Console
from rich.progress import track
from rich.prompt import Prompt
from rich.table import Table
from rich.theme import Theme

console = Console(record=True)

def get_search():
    return Prompt.ask("Search for an an airport")

def load_airport_json():
    # Load airport data from airports.json
    f = open('airports.json')

    airportData = json.load(f)
    
    return airportData

def find_matching_airports(name, airport_data):
    possible_matches = [airport for airport in airport_data \
                        if name.lower() in airport['name'].lower()]
    
    
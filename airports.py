import json
from datetime import datetime

import requests
from rich.console import Console
from rich.progress import track
from rich.prompt import Prompt
from rich.table import Table
from rich.theme import Theme

console = Console(record=True)

def get_search() -> str:
    """Prompts the user to enter an airport to search

    Returns:
        str: user's chosen airport
    """
    return Prompt.ask("Search for an an airport")

def load_airport_json() -> dict:
    """Opens airport.json file and loads it, to access airport data

    Returns:
        dict: Dictionary containing airports and information
    """
    f = open('airports.json')

    airportData = json.load(f)
    
    return airportData

def verify_user_airport_choice(possible_matches:list):
    airport_choices = [airports['name'] for airports in possible_matches]

    selection = None

    while selection == None:
        user_choice = Prompt.ask("Please select one out of: " + str(airport_choices))
        
        for airports in airport_choices:
            if user_choice.lower() == airports['name'].lower():
                selection = airports
                return selection
            

def find_matching_airports(name, airport_data):
    possible_matches = [airport for airport in airport_data \
                        if name.lower() in airport['name'].lower()]
    
    if len(possible_matches) == 0:
        console.print('Not a valid airport, please try again', style='bold red')
    elif len(possible_matches) == 1:
        console.print(possible_matches[0]['name'], style ='green')
    else:
        return verify_user_airport_choice(possible_matches)

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
        list: List of dictionaries containing airports and information
    """
    f = open('airports.json')

    airportData = json.load(f)
    
    return airportData

def verify_user_airport_choice(possible_matches:list) -> dict:
    """Takes a list of airports, and prompts user to select one from the list, returns one selection

    Args:
        possible_matches (list): List of airport dictionaries

    Returns:
        dict: Airport dictionary 
    """
    airport_choices = [airports['name'] for airports in possible_matches]

    match = None

    user_choice = Prompt.ask("Please select one out of: " + str(airport_choices))

    while match == None:
        user_choice = Prompt.ask("Invalid option, please select one of: " + str(airport_choices))
        
        for airports in airport_choices:
            if user_choice.lower() == airports['name'].lower():
                match = possible_matches[airports]
                console.print(f'You have selected: {(match["name"])}', style = 'green')
    
    return match           
            

def find_matching_airports(name: str, airport_data: list) -> dict:
    """Takes a name, and searches the name key in airport data, returns a single match

    Args:
        name (str): Airport name user entered
        airport_data (list): List containing airport dictionaries

    Returns:
        dict: Airport dictionary
    """
    possible_matches = [airport for airport in airport_data \
                        if name.lower() in airport['name'].lower()]
    
    if len(possible_matches) == 0:
        console.print('Not a valid airport, please try again', style='bold red')
    elif len(possible_matches) == 1:
        console.print(possible_matches[0]['name'], style ='green')
        return possible_matches[0]
    else:
        return verify_user_airport_choice(possible_matches)



if __name__ == "__main__":
    console.print(" ")
    console.print("✈️ ✈️ ✈️ ✈️ ✈️ ✈️ ✈️ ✈️")
    console.print("Welcome to the Airports Informer Tool")
    console.print("✈️ ✈️ ✈️ ✈️ ✈️ ✈️ ✈️ ✈️")
    console.print(" ")

    airportData = load_airport_json()

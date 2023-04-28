"""System module."""
import json
import os
#from datetime import datetime

import requests
from dotenv import load_dotenv
from rich.console import Console
# from rich.progress import track
from rich.prompt import Prompt
# from rich.table import Table
# from rich.theme import Theme

load_dotenv()

airport_api_key = os.environ['airport_api_key']
weather_api_key = os.environ['weather_api_key']

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
    with open('airports.json', encoding='utf-8') as airport_file:
        airport_list = json.load(airport_file)
    return airport_list

def verify_user_airport_choice(possible_matches:list) -> dict:
    """Takes a list of airports, and prompts user to select one from the list, 
    returns one selection

    Args:
        possible_matches (list): List of airport dictionaries

    Returns:
        dict: Airport dictionary 
    """
    airport_choices = [airports['name'] for airports in possible_matches]

    match = None

    while match is None:
        user_choice = Prompt.ask("Please select one out of: " + str(airport_choices) + '\n')
        for i, airports in enumerate(airport_choices):
            if user_choice.lower() == airports.lower():
                match = possible_matches[i]
                console.print(f'You have selected: {(match["name"])}', style = 'green')
    return match

def find_matching_airports_name(name: str, airport_list: list) -> dict:
    """Takes a name, and searches the name key in airport data, returns a single match

    Args:
        name (str): Airport name user entered
        airport_data (list): List containing airport dictionaries

    Returns:
        dict: Airport dictionary
    """
    possible_matches = [airport for airport in airport_list
                        if name.lower() in airport['name'].lower()]
    if len(possible_matches) == 0:
        console.print('Not a valid airport, please try again', style='bold red')
        return None
    if len(possible_matches) == 1:
        console.print(possible_matches[0]['name'], style ='green')
        return possible_matches[0]

    return verify_user_airport_choice(possible_matches)

def find_matching_airports_iata(iata: str, airport_list: list) -> dict:
    """Takes an Iata, and searches the Iata key in the airport data, returns a single match

    Args:
        iata (str): _description_
        airport_data (list): _description_

    Returns:
        dict: _description_
    """
    for airport in airport_list:
        if iata.upper() == str(airport['iata']).upper():
            return airport
    return None

def get_flights_from_iata(iata:str) -> json:
    """Searches airport API, using Iata for scheduled flights and returns JSON Object of 
    flights and data

    Args:
        iata (str): Airport Iata

    Returns:
        json: JSON Object containing flights and information of flights
    """
    return requests.get(f"https://airlabs.co/api/v9/schedules?dep_iata={iata}\
                        &api_key=f{airport_api_key}", timeout= 15).json()

def load_weather_for_location(lat: str, lng: str)-> json:
    """Takes in a longitude and latitude, and gets the current weather for the associated 
    location returns a json object containing data

    Args:
        lat (str): latitude of location
        lng (str): longitude of location

    Returns:
        json: JSON Object containing weather information
    """
    return requests.get(f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}=\
                        {lat},{lng}", timeout= 15).json()

def get_airport_data_value(airport: dict, key: str)-> str:
    """Takes an airport dict, and returns a value based on key

    Args:
        airport (dict): Airport Dict containing information about airport
        key (str): Dict key that needs to be accessed

    Returns:
        str: Dict Value
    """
    value = airport[key]

    if value is not None:
        return value

    return None

def get_weather_data_destination(iata: str, airport_list: list) -> json:
    """Takes Iata, finds the airport, and gets the longitude and latitude, returns
    a json object with weather data

    Args:
        iata (str): Airport Iata from list of flights
        airport_list (list): List of airports, containing data about airport

    Returns:
        json: JSON Object containing weather data from weather API
    """
    destination_airport = find_matching_airports_iata(iata, airport_list)

    destination_lat = get_airport_data_value(destination_airport, 'lat')
    destination_lon = get_airport_data_value(destination_airport, 'lon')

    return load_weather_for_location(destination_lat, destination_lon)

if __name__ == "__main__":
    console.print(" ")
    console.print("✈️ ✈️ ✈️ ✈️ ✈️ ✈️ ✈️ ✈️")
    console.print("Welcome to the Airports Informer Tool")
    console.print("✈️ ✈️ ✈️ ✈️ ✈️ ✈️ ✈️ ✈️")
    console.print(" ")

    airport_data = load_airport_json()

    while 1:
        AIRPORT_SEARCH = get_search()
        users_selection = find_matching_airports_name(AIRPORT_SEARCH, airport_data)

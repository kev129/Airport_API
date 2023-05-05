"""System module."""
import json
import os
from typing import NoReturn

import requests
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import track
from rich.prompt import Prompt
from rich.table import Table

# pylint: disable=C0303,W0702,C0103

load_dotenv()

airport_api_key = os.environ["airport_api_key"]
weather_api_key = os.environ["weather_api_key"]
console = Console(record=True)

def get_search() -> str:
    """Prompts the user to enter an airport to search

    Returns:
        str: user"s chosen airport
    """
    return Prompt.ask("Search for an an airport")

def load_airport_data() -> dict:
    """Opens airport.json file and loads it, to access airport data. Data structure: {
    "name": "",
    "city": "",
    "country": "",
    "IATA": "",
    "icao": "",
    "lat": "",
    "lon": "",
    "timezone": ""
  }

    Returns:
        list: List of dictionaries containing airports and information
    """
    with open("airports2.json", encoding="utf-8") as airport_file:
        airport_list = json.load(airport_file)
    return airport_list

def select_airport_from_list(possible_matches:list[dict]) -> dict:
    """Takes a list of airports, and prompts user to select one from the list, 
    returns one selection

    Args:
        possible_matches (list): List of airport dictionaries

    Returns:
        dict: Airport dictionary 
    """
    airport_choices = [airports["name"].strip() for airports in possible_matches]

    while True:
        user_choice = Prompt.ask("Please select one out of: " + str(airport_choices) + "\n").strip().lower()
        for i, airports in enumerate(airport_choices):
            if user_choice == airports.lower():
                match = possible_matches[i]
                console.print(f"You have selected: {(match['name'])}", style = "green")
                return match
        console.print("Invalid selection please try again, enter the full airport name",
                      style = "red")

def find_airports_by_name(name: str, airport_list: list[dict]) -> dict:
    """Takes a name, and searches the name key in airport data, returns a single match

    Args:
        name (str): Airport name user entered
        airport_data (list): List containing airport dictionaries

    Returns:
        dict: Airport dictionary
    """
    possible_matches = [airport for airport in airport_list
                        if name.lower() in airport["name"].lower()]
    if len(possible_matches) == 0:
        console.print("Not a valid airport, please try again", style="bold red")
        return None
    if len(possible_matches) == 1:
        console.print(possible_matches[0]["name"], style ="green")
        return possible_matches[0]

    return select_airport_from_list(possible_matches)

def find_airports_by_icao(icao: str, airport_list: list[dict]) -> dict:
    """Takes an Icao, and searches the Icao key in the airport data, returns a single match

    Args:
        Icao (str): The ICAO code of the airport to search for.
        airport_data (list): List containing airport dictionaries

    Returns:
        dict: Airport dictionary
    """
    for airport in airport_list:
        if icao.upper() == str(airport["icao"]).upper():
            return airport
    return None

def get_scheduled_flights_from_icao(icao:str) -> json:
    """Searches airport API, using icao for scheduled flights and returns JSON Object of 
    flights and data

    Args:
        Icao (str): Airport Icao

    Returns:
        json: JSON Object containing flights and information of flights
    """
    try:
        response = requests.get(f"https://airlabs.co/api/v9/schedules?dep_icao={icao}&api_key="
                        f"{airport_api_key}", timeout= 15).json()
    except requests.exceptions.Timeout:
        print("Request timed out. Please try again later.")

    except requests.exceptions.ConnectionError:
        print("Failed to connect to server. Please check your internet connection and try again.")

    except requests.exceptions.RequestException as error:
        print(f"An error occurred while making the request: {error}")

    return response

def get_current_weather_for_location(lat: str, lng: str)-> json:
    """Takes in a longitude and latitude, and gets the current weather for the associated 
    
    location returns a json object containing data

    Args:
        lat (str): latitude of location
        lng (str): longitude of location

    Returns:
        json: JSON Object containing weather information
    """
    try:
        response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}="
                        f"{lat},{lng}", timeout= 15).json()
    
    except requests.exceptions.Timeout:
        print("Request timed out. Please try again later.")

    except requests.exceptions.ConnectionError:
        print("Failed to connect to server. Please check your internet connection and try again.")

    except requests.exceptions.RequestException as error:
        print(f"An error occurred while making the request: {error}")

    return response

def get_airport_data_by_key(airport: dict, key: str)-> str:
    """Takes an airport dict, and returns a value based on key

    Args:
        airport (dict): Airport Dict containing information about airport
        key (str): Dict key that needs to be accessed

    Returns:
        str: Dict Value
    """
    value = airport[key]
    return value

def get_weather_data_for_destination(icao: str, airport_list: list) -> json:
    """Takes Icao, finds the airport, and gets the longitude and latitude, returns
    a json object with weather data

    Args:
        icao (str): Airport Icao from list of flights
        airport_list (list): List of airports, containing data about airport

    Returns:
        json: JSON Object containing weather data from weather API
    """
    destination_airport = find_airports_by_icao(icao, airport_list)

    destination_lat = get_airport_data_by_key(destination_airport, "lat")
    destination_lon = get_airport_data_by_key(destination_airport, "lon")

    return get_current_weather_for_location(destination_lat, destination_lon)

def get_current_temperature(data:dict) -> str:
    """Takes the destination dict, and returns the current temperature

    Args:
        data (dict): Location dict containing information about location

    Returns:
        str: Temperature of location degrees c
    """
    return data["current"]["temp_c"]

def get_current_weather(data:dict) -> str:
    """Takes the destination dict, and returns the current weather condition

    Args:
        data (dict): Location dict containing information about location

    Returns:
        str: Weather condition
    """
    return data["current"]["condition"]["text"]

def render_flights(flights: dict, airport_list: list) -> NoReturn:
    """Takes in list of flights for a given airport, builds table with 
    information about flight, and destination weather

    Args:
        flights (dict): Dict of request and response, including list of flights 
        dicts from airport API
        airport_list (list): List of airports from airport JSON

    Returns:
        NoReturn: Returns nothing
    """
    table = Table(title="Flights")

    table.add_column("Flight No.", justify="right", style="cyan", no_wrap=True)
    table.add_column("Departure time", style="blue")
    table.add_column("Destination", style="magenta")
    table.add_column("Delayed? (Minutes)", justify="right", style="green")
    table.add_column("Weather", justify="right", style="yellow")

    flight_response = flights["response"]
    for flight in track(flight_response, description= "Searching..."):
        arrival_icao = flight["arr_icao"]
        print(f"Checking {arrival_icao}...")
        weather_data = get_weather_data_for_destination(arrival_icao,airport_list)

        destination_temperature = get_current_temperature(weather_data)
        destination_weather_text = get_current_weather(weather_data)
        destination_name = find_airports_by_icao(flight["arr_icao"], airport_data)['name']

        table.add_row(flight["flight_number"], flight["dep_time"], destination_name,
                    str(flight["delayed"]), str(destination_temperature)+ '°C' + ' - ' +
                    destination_weather_text)
        
    console.print(table)

if __name__ == "__main__":
    console.print(" ")
    console.print("✈️ ✈️ ✈️ ✈️ ✈️ ✈️ ✈️ ✈️")
    console.print("Welcome to the Airports Informer Tool")
    console.print("✈️ ✈️ ✈️ ✈️ ✈️ ✈️ ✈️ ✈️")
    console.print(" ")

    airport_data = load_airport_data()

    while 1:
        search_term = get_search()
        users_selection = find_airports_by_name(search_term, airport_data)
        
        if users_selection is None:
            continue

        departure_icao = users_selection['icao']
        departure_airport = find_airports_by_icao(departure_icao, airport_data)
        user_airport_flights= get_scheduled_flights_from_icao(departure_icao)
        render_flights(user_airport_flights,airport_data)

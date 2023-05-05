# Airport Flight Weather Information

This script is a Python module that allows you to search for airport information, flights information, and weather information for a given airport. It uses two API's to retrieve flight and weather data. It is also dependent on the `dotenv`, `requests`, `rich`, and `typing` libraries.

## Getting started

To use this module, you need to have API keys from both `airlabs` and `weatherapi.com`. The module uses the `dotenv` library to securely store your API keys in a `.env` file in the root directory. For example, your `.env` file should contain:

```
airport_api_key=<your_airlabs_api_key>
weather_api_key=<your_weatherapi_key>
```

Please ensure that you add `.env` to your `.gitignore` file to prevent your API keys from being exposed on a public repository.

## Usage

To use this module, follow these steps:

1. Clone the repository or download the `airport.py` file and place it in your project directory.
2. Install the required libraries: `pip install -r requirements.txt`
3. Import the module and use the available functions.

### Available functions:

1. `get_search()`: This function prompts the user to enter an airport to search and returns the user's choice as a string.
2. `load_airport_json()`: This function loads a JSON file (`airports.json`) containing airport data.
3. `verify_user_airport_choice(possible_matches: list)`: This function prompts the user to select an airport from a list of airports and returns the selected airport as a dictionary.
4. `find_matching_airports_name(name: str, airport_list: list)`: This function searches for an airport in the airport list using the name of the airport and returns the airport data as a dictionary.
5. `find_matching_airports_icao(icao: str, airport_list: list)`: This function searches for an airport in the airport list using the ICAO code of the airport and returns the airport data as a dictionary.
6. `get_flights_from_icao(icao: str)`: This function searches for scheduled flights from the airport using the ICAO code and returns the flight data as a JSON object.
7. `load_weather_for_location(lat: str, lng: str)`: This function retrieves the current weather data for a given location using the longitude and latitude and returns the weather data as a JSON object.
8. `get_airport_data_value(airport: dict, key: str)`: This function returns the value of a given key in an airport data dictionary.
9. `get_weather_data_destination(icao: str, airport_list: list)`: This function retrieves the weather data for the destination airport of a given flight using the airport list and returns the weather data as a JSON object.
10. `get_temperature_destination(data:dict)`: This function returns the current temperature for a given location.

## Example

Here is an example usage of this module:

```python
import airport

# Load airport data
airport_list = airport.load_airport_json()

# Get airport to search
airport_name = airport.get_search()

# Find matching airports
airport_data = airport.find_matching_airports_name(airport_name, airport_list)

# Get flights from the airport
flights = airport.get_flights_from_icao(airport_data["icao"])

# Get weather data for destination
destination_weather = airport.get_weather_data_destination(flights["data"][0]["flight"]["arrival"]["icao"], airport_list)

# Print temperature for destination
temperature = airport.get_temperature_destination(destination_weather)
print(f"Temperature at the destination airport is {temperature} degrees Celsius")
```

## Note

This module uses two API's.

Source for airport.json https://gist.github.com/tdreyno/4278655 .

Source for airport2.json https://www.pureleapfrog.org/aer-lingus/carbon-neutral/airports-json/ .

airports2.json contains all airports, the first json doesn't contain all airports and may lead to "Nonetype object not subscriptable", as the function `find_matching_airports_icao(icao: str, airport_list: list)` returns None

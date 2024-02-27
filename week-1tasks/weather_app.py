import requests
import json
import time

API_KEY = "adcdf6a3e76a5f6008d05f8b6df31d30"  # Replace with your actual API key from OpenWeatherMap
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

FAVORITE_CITIES_FILE = 'favorite_cities.json'


def save_favorite_cities(favorite_cities):
    with open(FAVORITE_CITIES_FILE, 'w') as file:
        json.dump(favorite_cities, file)


def load_favorite_cities():
    try:
        with open(FAVORITE_CITIES_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return []


def add_favorite_city(city):
    favorite_cities = load_favorite_cities()
    if city not in favorite_cities:
        favorite_cities.append(city)
        save_favorite_cities(favorite_cities)
        print(f"{city} added to favorites.")
    else:
        print(f"{city} is already in favorites.")


def remove_favorite_city(city):
    favorite_cities = load_favorite_cities()
    if city in favorite_cities:
        favorite_cities.remove(city)
        save_favorite_cities(favorite_cities)
        print(f"{city} removed from favorites.")
    else:
        print(f"{city} is not found in favorites.")


def list_favorite_cities():
    favorite_cities = load_favorite_cities()
    if favorite_cities:
        print("Favorite Cities:")
        for city in favorite_cities:
            print(f"- {city}")
    else:
        print("No favorite cities yet.")


def get_weather(city):
    params = {'q': city, 'appid': API_KEY}
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        weather_data = response.json()
        return weather_data
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None


def display_weather(weather):
    if weather and weather.get('main'):
        print(f"Weather in {weather['name']}, {weather['sys']['country']}:")
        print(f"Temperature: {weather['main']['temp']} K")  # Temperature is in Kelvin
        print(f"Condition: {weather['weather'][0]['description']}")
        print(f"Wind Speed: {weather['wind']['speed']} m/s")
    else:
        print("Weather data not available.")


def refresh_weather(city):
    while True:
        weather = get_weather(city)
        display_weather(weather)
        time.sleep(15)  # Adjust refresh interval as needed


def main():
    print("Welcome to the Weather Checking Application!")
    city = input("Enter city name: ")

    # Initial weather check
    weather = get_weather(city)
    display_weather(weather)

    # CRUD operations for favorite cities
    favorite_option = input("Do you want to manage favorite cities? (y/n): ").lower()
    if favorite_option == 'y':
        while True:
            print("\nFavorite Cities Management:")
            print("1. Add Favorite City")
            print("2. Remove Favorite City")
            print("3. List Favorite Cities")
            print("4. Continue")
            choice = input("Enter your choice (1-4): ")

            if choice == '1':
                city_to_add = input("Enter the city to add to favorites: ")
                add_favorite_city(city_to_add)
            elif choice == '2':
                city_to_remove = input("Enter the city to remove from favorites: ")
                remove_favorite_city(city_to_remove)
            elif choice == '3':
                list_favorite_cities()
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")

    # Continuous refresh
    refresh_option = input("Do you want to enable auto-refresh? (y/n): ").lower()
    if refresh_option == 'y':
        refresh_weather(city)


if __name__ == "__main__":
    main()


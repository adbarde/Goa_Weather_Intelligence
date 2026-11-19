
"""
File Name: weather_api.py
Project: Goa Weather Prediction and Activity Planner

Purpose:
Fetches current weather information and additional
weather conditions from the Open-Meteo Forecast API.
"""

import requests
import pandas as pd

from config import (
    LOCATIONS,
    FORECAST_API_URL,
    TIMEZONE
)


# --------------------------------------------------
# GET NEAREST HOURLY WEATHER VALUE
# --------------------------------------------------

def get_hourly_value(hourly_data, variable, current_time):

    """
    Retrieves the hourly value closest to the
    current weather observation time.
    """

    times = hourly_data.get("time", [])

    values = hourly_data.get(variable, [])

    if len(times) == 0 or len(values) == 0:
        return None

    if len(times) != len(values):
        return None

    target_time = pd.to_datetime(current_time)

    hourly_times = pd.to_datetime(times)

    differences = abs(hourly_times - target_time)

    nearest_index = differences.argmin()

    value = values[nearest_index]

    if pd.isna(value):
        return None

    return float(value)


# --------------------------------------------------
# FETCH CURRENT WEATHER DATA
# --------------------------------------------------

def fetch_weather(location):

    """
    Fetches current weather data for a selected
    Goa location.

    Parameters:
        location: Name of the selected Goa location.

    Returns:
        Pandas DataFrame containing weather data.
    """

    # Validate location
    if location not in LOCATIONS:

        raise ValueError(
            "Invalid Goa location selected."
        )

    # Get location coordinates
    latitude = LOCATIONS[location]["latitude"]

    longitude = LOCATIONS[location]["longitude"]

    # API parameters
    params = {

        "latitude": latitude,

        "longitude": longitude,

        # Current weather variables
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "wind_speed_10m",
            "wind_direction_10m",
            "wind_gusts_10m",
            "pressure_msl",
            "cloud_cover",
            "weather_code"
        ],

        # Hourly weather variables
        "hourly": [
            "uv_index",
            "precipitation_probability",
            "visibility"
        ],

        # Measurement units
        "temperature_unit": "celsius",

        "wind_speed_unit": "kmh",

        "precipitation_unit": "mm",

        # Local timezone
        "timezone": TIMEZONE,

        # Forecast duration
        "forecast_days": 1
    }

    try:

        # Send API request
        response = requests.get(
            FORECAST_API_URL,
            params=params,
            timeout=20
        )

        # Check API response
        response.raise_for_status()

        # Convert JSON response into dictionary
        data = response.json()

        # Extract current weather
        current = data["current"]

        # Extract hourly weather
        hourly = data["hourly"]

        current_time = current["time"]

        # Retrieve additional hourly values
        uv_index = get_hourly_value(
            hourly,
            "uv_index",
            current_time
        )

        precipitation_probability = get_hourly_value(
            hourly,
            "precipitation_probability",
            current_time
        )

        visibility = get_hourly_value(
            hourly,
            "visibility",
            current_time
        )

        # Prepare weather information
        weather_data = {

            "time": current_time,

            # Original weather variables
            "temperature_2m":
                current["temperature_2m"],

            "relative_humidity_2m":
                current["relative_humidity_2m"],

            "precipitation":
                current["precipitation"],

            "wind_speed_10m":
                current["wind_speed_10m"],

            "pressure_msl":
                current["pressure_msl"],

            # Additional weather variables
            "apparent_temperature":
                current.get("apparent_temperature"),

            "wind_direction_10m":
                current.get("wind_direction_10m"),

            "wind_gusts_10m":
                current.get("wind_gusts_10m"),

            "cloud_cover":
                current.get("cloud_cover"),

            "weather_code":
                current.get("weather_code"),

            "uv_index":
                uv_index,

            "precipitation_probability":
                precipitation_probability,

            "visibility":
                visibility,

            # Location information
            "location": location,

            "latitude": latitude,

            "longitude": longitude
        }

        # Convert dictionary into DataFrame
        df = pd.DataFrame([weather_data])

        return df

    except requests.exceptions.Timeout:

        raise Exception(
            "Weather API request timed out. Please try again."
        )

    except requests.exceptions.ConnectionError:

        raise Exception(
            "Unable to connect to the weather service. "
            "Check your internet connection."
        )

    except requests.exceptions.HTTPError:

        raise Exception(
            "Weather API returned an error response."
        )

    except requests.exceptions.RequestException:

        raise Exception(
            "An error occurred while requesting weather data."
        )

    except (KeyError, TypeError, ValueError):

        raise Exception(
            "Unable to process the weather data received."
        )


# --------------------------------------------------
# TEST WEATHER API
# --------------------------------------------------

if __name__ == "__main__":

    location = "Panaji"

    print("Fetching weather data for:", location)

    try:

        weather_df = fetch_weather(location)

        print("\nCURRENT WEATHER DATA")
        print("--------------------")

        print(weather_df.to_string(index=False))

    except Exception as error:

        print("Error:", error)

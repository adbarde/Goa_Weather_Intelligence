
"""
File Name: config.py
Project: Goa Weather Prediction and Activity Planner

Purpose:
Stores application configuration, Goa locations,
API endpoints, and model feature definitions.
"""

# --------------------------------------------------
# GOA LOCATIONS
# --------------------------------------------------

LOCATIONS = {
    "Panaji": {
        "latitude": 15.4909,
        "longitude": 73.8278
    },
    "Mapusa": {
        "latitude": 15.5915,
        "longitude": 73.8080
    },
    "Pernem": {
        "latitude": 15.7230,
        "longitude": 73.7950
    },
    "Bicholim": {
        "latitude": 15.5991,
        "longitude": 73.9457
    },
    "Valpoi": {
        "latitude": 15.5324,
        "longitude": 74.1367
    },
    "Ponda": {
        "latitude": 15.4010,
        "longitude": 74.0124
    },
    "Vasco da Gama": {
        "latitude": 15.3860,
        "longitude": 73.8440
    },
    "Margao": {
        "latitude": 15.2832,
        "longitude": 73.9862
    },
    "Quepem": {
        "latitude": 15.2120,
        "longitude": 74.0770
    },
    "Canacona": {
        "latitude": 14.9959,
        "longitude": 74.0467
    }
}


# --------------------------------------------------
# API CONFIGURATION
# --------------------------------------------------

FORECAST_API_URL = (
    "https://api.open-meteo.com/v1/forecast"
)

ARCHIVE_API_URL = (
    "https://archive-api.open-meteo.com/v1/archive"
)

TIMEZONE = "Asia/Kolkata"


# --------------------------------------------------
# WEATHER VARIABLES
# --------------------------------------------------

WEATHER_VARIABLES = [
    "temperature_2m",
    "relative_humidity_2m",
    "precipitation",
    "wind_speed_10m",
    "pressure_msl"
]


# --------------------------------------------------
# MODEL CONFIGURATION
# --------------------------------------------------

MODEL_FILE = "weather_model.joblib"

FEATURES = [
    "relative_humidity_2m",
    "precipitation",
    "wind_speed_10m",
    "pressure_msl",
    "hour_sin",
    "hour_cos",
    "month_sin",
    "month_cos",
    "latitude",
    "longitude"
]

TARGET = "temperature_2m"


# --------------------------------------------------
# APPLICATION CONFIGURATION
# --------------------------------------------------

APP_TITLE = "Goa Weather Intelligence"

APP_ICON = "🌤️"

PAGE_LAYOUT = "wide"

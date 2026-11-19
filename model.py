
"""
File Name: model.py
Project: Goa Weather Prediction and Activity Planner

Purpose:
Loads the trained Batch Gradient Descent model,
prepares live weather features, predicts temperature,
and provides model evaluation metrics.
"""

import joblib
import numpy as np
import pandas as pd

from pathlib import Path
from functools import lru_cache

from config import MODEL_FILE, FEATURES


# --------------------------------------------------
# LOAD TRAINED MODEL
# --------------------------------------------------

@lru_cache(maxsize=1)
def load_model():

    """
    Loads the saved model package.

    Returns:
        Dictionary containing weights, bias,
        scaler, features and evaluation metrics.
    """

    model_path = Path(__file__).resolve().parent / MODEL_FILE

    if not model_path.exists():
        raise FileNotFoundError(
            "Model file not found: " + str(model_path)
        )

    model_package = joblib.load(model_path)

    required_keys = [
        "weights",
        "bias",
        "scaler",
        "features",
        "metrics"
    ]

    for key in required_keys:
        if key not in model_package:
            raise ValueError(
                "Model package is missing: " + key
            )

    # Verify feature order
    if list(model_package["features"]) != FEATURES:
        raise ValueError(
            "Model features do not match config.py. "
            "Check the feature names and their order."
        )

    return model_package


# --------------------------------------------------
# FEATURE ENGINEERING
# --------------------------------------------------

def prepare_features(weather_df):

    """
    Prepares the input features required by the model.

    Parameters:
        weather_df: DataFrame containing current
                    weather information.

    Returns:
        DataFrame containing the 10 model features.
    """

    if weather_df.empty:
        raise ValueError("Weather data is empty.")

    df = weather_df.copy()

    # Convert API timestamp into datetime
    df["time"] = pd.to_datetime(df["time"])

    # Extract hour and month
    hour = df["time"].dt.hour
    month = df["time"].dt.month

    # Cyclical time features
    df["hour_sin"] = np.sin(
        2 * np.pi * hour / 24
    )

    df["hour_cos"] = np.cos(
        2 * np.pi * hour / 24
    )

    df["month_sin"] = np.sin(
        2 * np.pi * month / 12
    )

    df["month_cos"] = np.cos(
        2 * np.pi * month / 12
    )

    # Select features in exact training order
    X = df[FEATURES].copy()

    return X


# --------------------------------------------------
# TEMPERATURE PREDICTION
# --------------------------------------------------

def predict_temperature(weather_df):

    """
    Predicts temperature using Batch Gradient Descent.

    Parameters:
        weather_df: Current weather DataFrame.

    Returns:
        Dictionary containing predicted temperature,
        actual temperature and absolute error.
    """

    # Load trained model
    model_package = load_model()

    weights = np.asarray(
        model_package["weights"]
    )

    bias = model_package["bias"]

    scaler = model_package["scaler"]

    # Prepare input features
    X = prepare_features(weather_df)

    # Apply the saved training scaler
    X_scaled = scaler.transform(X)

    # Batch Gradient Descent prediction equation
    prediction = np.dot(
        X_scaled,
        weights
    ) + bias

    predicted_temperature = float(prediction[0])

    # Actual temperature from the weather API
    actual_temperature = float(
        weather_df.iloc[0]["temperature_2m"]
    )

    # Calculate live prediction error
    absolute_error = abs(
        actual_temperature - predicted_temperature
    )

    return {
        "predicted_temperature": predicted_temperature,
        "actual_temperature": actual_temperature,
        "absolute_error": absolute_error
    }


# --------------------------------------------------
# MODEL EVALUATION METRICS
# --------------------------------------------------

def get_model_metrics():

    """
    Returns the historical test metrics
    calculated during model evaluation in Colab.
    """

    model_package = load_model()

    return model_package["metrics"]


# --------------------------------------------------
# TEST MODEL
# --------------------------------------------------

if __name__ == "__main__":

    from weather_api import fetch_weather

    location = "Panaji"

    try:

        print("Fetching current weather data...")

        weather_df = fetch_weather(location)

        print("\nPreparing model features...")

        features = prepare_features(weather_df)

        print("\nMODEL INPUT FEATURES")
        print("--------------------")
        print(features.to_string(index=False))

        print("\nPredicting temperature...")

        result = predict_temperature(weather_df)

        print("\nPREDICTION RESULTS")
        print("------------------")

        print(
            "Predicted Temperature:",
            round(result["predicted_temperature"], 2),
            "°C"
        )

        print(
            "Actual Temperature:",
            round(result["actual_temperature"], 2),
            "°C"
        )

        print(
            "Absolute Error:",
            round(result["absolute_error"], 2),
            "°C"
        )

        print("\nHISTORICAL MODEL EVALUATION")
        print("---------------------------")

        metrics = get_model_metrics()

        for name, value in metrics.items():
            print(name + ":", value)

    except Exception as error:

        print("Error:", error)

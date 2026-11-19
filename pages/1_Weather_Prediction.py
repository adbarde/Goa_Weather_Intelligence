
"""
File Name: 1_Weather_Prediction.py
Project: Goa Weather Prediction and Activity Planner

Purpose:
Displays current weather information and predicted
temperature for selected locations in Goa.
"""

import streamlit as st
import pandas as pd

from config import LOCATIONS
from weather_api import fetch_weather
from model import (
    predict_temperature,
    get_model_metrics
)

from style import (
    apply_custom_style,
    render_header,
    render_footer
)
# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Weather Prediction",
    page_icon="🌤️",
    layout="wide"
)
apply_custom_style()
render_header(
    "Weather Prediction",
    "Temperature estimation using Machine Learning"
)
# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------



st.write(
    """
    Select a location in Goa to retrieve current weather
    information and estimate its temperature using the
    trained Batch Gradient Descent model.
    """
)

st.divider()


# --------------------------------------------------
# LOCATION SELECTION
# --------------------------------------------------

st.subheader("Select Location")

location = st.selectbox(
    "Choose a Goa location",
    list(LOCATIONS.keys())
)


# --------------------------------------------------
# FETCH WEATHER DATA
# --------------------------------------------------

if st.button("Fetch Weather Data", type="primary"):

    with st.spinner("Fetching current weather data..."):

        try:

            weather_df = fetch_weather(location)

            st.session_state["weather_df"] = weather_df
            st.session_state["selected_location"] = location

        except Exception as error:

            st.error(str(error))


# --------------------------------------------------
# DISPLAY WEATHER AND PREDICTION
# --------------------------------------------------

if (
    "weather_df" in st.session_state
    and st.session_state.get("selected_location") == location
):

    weather_df = st.session_state["weather_df"]

    st.divider()

    st.subheader(
        "Current Weather - " + location
    )

    weather = weather_df.iloc[0]

    st.caption(
        "Observation time: " + str(weather["time"])
    )

    # --------------------------------------------------
    # CURRENT WEATHER METRICS
    # --------------------------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Actual Temperature",
        str(round(weather["temperature_2m"], 2)) + " °C"
    )

    col2.metric(
        "Humidity",
        str(weather["relative_humidity_2m"]) + " %"
    )

    col3.metric(
        "Precipitation",
        str(weather["precipitation"]) + " mm"
    )

    col4, col5 = st.columns(2)

    col4.metric(
        "Wind Speed",
        str(weather["wind_speed_10m"]) + " km/h"
    )

    col5.metric(
        "Atmospheric Pressure",
        str(weather["pressure_msl"]) + " hPa"
    )

    # --------------------------------------------------
    # TEMPERATURE PREDICTION
    # --------------------------------------------------

    st.divider()

    st.subheader("Temperature Prediction")

    try:

        result = predict_temperature(weather_df)

        predicted_temperature = result[
            "predicted_temperature"
        ]

        actual_temperature = result[
            "actual_temperature"
        ]

        absolute_error = result[
            "absolute_error"
        ]

        prediction_col, actual_col, error_col = st.columns(3)

        prediction_col.metric(
            "Predicted Temperature",
            f"{predicted_temperature:.2f} °C"
        )

        actual_col.metric(
            "Actual Temperature",
            f"{actual_temperature:.2f} °C"
        )

        error_col.metric(
            "Absolute Error",
            f"{absolute_error:.2f} °C"
        )

        # --------------------------------------------------
        # ACTUAL VS PREDICTED COMPARISON
        # --------------------------------------------------

        st.subheader("Actual vs Predicted Temperature")

        comparison_df = pd.DataFrame({
            "Temperature Type": [
                "Actual Temperature",
                "Predicted Temperature"
            ],
            "Temperature (°C)": [
                actual_temperature,
                predicted_temperature
            ]
        })
        st.bar_chart(
            comparison_df.set_index("Temperature Type"),
            color="#EB110B"
        )

        # --------------------------------------------------
        # HISTORICAL MODEL EVALUATION
        # --------------------------------------------------

        st.divider()

        st.subheader("Model Evaluation")

        st.caption(
            "Historical test-set performance from model "
            "evaluation in Google Colab."
        )

        metrics = get_model_metrics()

        metric_col1, metric_col2 = st.columns(2)
        metric_col3, metric_col4 = st.columns(2)

        metric_col1.metric(
            "MAE",
            f"{metrics['MAE']:.4f}"
        )

        metric_col2.metric(
            "MSE",
            f"{metrics['MSE']:.4f}"
        )

        metric_col3.metric(
            "RMSE",
            f"{metrics['RMSE']:.4f}"
        )

        metric_col4.metric(
            "R² Score",
            f"{metrics['R2']:.4f}"
        )

        # --------------------------------------------------
        # PREDICTION INTERPRETATION
        # --------------------------------------------------

        st.divider()

        st.subheader("Prediction Analysis")

        if absolute_error <= 1:

            st.success(
                "The predicted temperature is close "
                "to the actual temperature."
            )

        elif absolute_error <= 2:

            st.info(
                "The prediction shows a moderate "
                "difference from the actual temperature."
            )

        else:

            st.warning(
                "The prediction differs noticeably "
                "from the actual temperature."
            )

        st.caption(
            "The live absolute error represents one observation. "
            "Historical MAE, MSE, RMSE and R² are calculated "
            "using the separate historical test dataset."
        )

    except Exception as error:

        st.error(
            "Unable to generate temperature prediction: "
            + str(error)
        )

else:

    st.info(
        "Select a Goa location and click "
        "'Fetch Weather Data' to begin."
    )


    
render_footer()
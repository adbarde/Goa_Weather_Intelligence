
"""
Page: Activity Suggestions
Project: Goa Weather Prediction and Activity Planner

Purpose:
Displays weather-based activity recommendations
with suitability scores and explanations.
"""

import streamlit as st
import pandas as pd

from config import LOCATIONS

from weather_api import fetch_weather

from model import predict_temperature

from activity_planner import generate_activity_plan
from style import (
    apply_custom_style,
    render_header,
    render_footer
)

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Activity Planner",
    page_icon="🌤️",
    layout="wide"
)

apply_custom_style()
render_header(
    "Activity Planner",
    "Weather-based outdoor activity recommendations"
)

# --------------------------------------------------
# HELPER FUNCTION
# --------------------------------------------------

def display_value(value, unit=""):

    """
    Displays numerical values safely.
    """

    if value is None:

        return "Unavailable"

    try:

        if pd.isna(value):

            return "Unavailable"

        return str(round(float(value), 2)) + unit

    except (TypeError, ValueError):

        return "Unavailable"


# --------------------------------------------------
# DISPLAY ACTIVITY RESULTS
# --------------------------------------------------

def display_activities(activities):

    """
    Displays activity scores and explanations.
    """

    for activity in activities:

        with st.expander(
            activity["name"]
            + " - "
            + str(activity["score"])
            + "/100"
        ):

            st.progress(
                activity["score"] / 100
            )

            st.write(
                "**Suitability:**",
                activity["status"]
            )

            st.write("**Explanation:**")

            for reason in activity["reasons"]:

                st.write("- " + reason)


# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

st.write(
    "Get activity recommendations based on "
    "weather conditions in Goa."
)

st.write(
    "The planner evaluates temperature, humidity, "
    "rainfall, wind, UV exposure and visibility."
)


# --------------------------------------------------
# LOCATION SELECTION
# --------------------------------------------------

location = st.selectbox(
    "Select Goa Location",
    list(LOCATIONS.keys())
)


# --------------------------------------------------
# CLEAR OLD RESULTS WHEN LOCATION CHANGES
# --------------------------------------------------

if (
    "activity_location" in st.session_state
    and st.session_state["activity_location"] != location
):

    st.session_state.pop("activity_weather", None)

    st.session_state.pop("activity_prediction", None)

    st.session_state.pop("activity_plan", None)

    st.session_state.pop("activity_location", None)


# --------------------------------------------------
# GENERATE ACTIVITY PLAN
# --------------------------------------------------

if st.button(
    "Generate Activity Suggestions",
    type="primary"
):

    try:

        with st.spinner(
            "Fetching weather data and evaluating activities..."
        ):

            # --------------------------------------
            # FETCH CURRENT WEATHER
            # --------------------------------------

            weather_df = fetch_weather(location)

            if weather_df is None or weather_df.empty:

                raise ValueError(
                    "No weather data was returned for this location."
                )

            # Get the first weather observation
            weather = weather_df.iloc[0]

            # --------------------------------------
            # PREDICT TEMPERATURE
            # --------------------------------------

            prediction = predict_temperature(weather_df)

            predicted_temperature = prediction[
                "predicted_temperature"
            ]

            # --------------------------------------
            # GENERATE ACTIVITY RECOMMENDATIONS
            # --------------------------------------

            plan = generate_activity_plan(

                predicted_temperature=predicted_temperature,

                humidity=weather["relative_humidity_2m"],

                precipitation=weather["precipitation"],

                wind_speed=weather["wind_speed_10m"],

                apparent_temperature=weather[
                    "apparent_temperature"
                ],

                precipitation_probability=weather[
                    "precipitation_probability"
                ],

                wind_gusts=weather["wind_gusts_10m"],

                uv_index=weather["uv_index"],

                visibility=weather["visibility"],

                cloud_cover=weather["cloud_cover"],

                weather_code=weather["weather_code"]

            )

            # --------------------------------------
            # SAVE RESULTS IN SESSION STATE
            # --------------------------------------

            st.session_state["activity_weather"] = weather_df

            st.session_state["activity_prediction"] = prediction

            st.session_state["activity_plan"] = plan

            st.session_state["activity_location"] = location

    except Exception as error:

        st.error(
            "Unable to generate activity suggestions: "
            + str(error)
        )


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

if (
    "activity_plan" in st.session_state
    and st.session_state.get("activity_location") == location
):

    weather_df = st.session_state["activity_weather"]

    prediction = st.session_state["activity_prediction"]

    plan = st.session_state["activity_plan"]

    weather = weather_df.iloc[0]

    st.divider()

    st.subheader(
        "Weather Information - " + location
    )

    st.caption(
        "Observation time: " + str(weather["time"])
    )

    # ----------------------------------------------
    # WEATHER METRICS
    # ----------------------------------------------

    st.markdown("### Temperature")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Predicted Temperature",
        display_value(
            prediction["predicted_temperature"],
            " °C"
        )
    )

    col2.metric(
        "Actual Temperature",
        display_value(
            weather["temperature_2m"],
            " °C"
        )
    )

    col3.metric(
        "Feels Like",
        display_value(
            weather["apparent_temperature"],
            " °C"
        )
    )

    st.markdown("### Atmospheric Conditions")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Humidity",
        display_value(
            weather["relative_humidity_2m"],
            "%"
        )
    )

    col2.metric(
        "Precipitation",
        display_value(
            weather["precipitation"],
            " mm"
        )
    )

    col3.metric(
        "Rain Probability",
        display_value(
            weather["precipitation_probability"],
            "%"
        )
    )

    st.markdown("### Wind and Sun Exposure")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Wind Speed",
        display_value(
            weather["wind_speed_10m"],
            " km/h"
        )
    )

    col2.metric(
        "Wind Gusts",
        display_value(
            weather["wind_gusts_10m"],
            " km/h"
        )
    )

    col3.metric(
        "UV Index",
        display_value(
            weather["uv_index"]
        )
    )

    st.markdown("### Visibility and Sky Conditions")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Cloud Cover",
        display_value(
            weather["cloud_cover"],
            "%"
        )
    )

    visibility_km = weather["visibility"]

    if visibility_km is not None:

        try:

            if not pd.isna(visibility_km):

                visibility_km = float(visibility_km) / 1000

            else:

                visibility_km = None

        except (TypeError, ValueError):

            visibility_km = None

    col2.metric(
        "Visibility",
        display_value(
            visibility_km,
            " km"
        )
    )

    col3.metric(
        "Weather Condition",
        plan["weather_description"]
    )

    # ----------------------------------------------
    # OVERALL WEATHER CONDITION
    # ----------------------------------------------

    st.divider()

    st.subheader("Overall Activity Conditions")

    st.write(
        "**Temperature Classification:**",
        plan["temperature_condition"]
    )

    condition = plan["overall_condition"]

    if condition == "Generally Favourable":

        st.success(condition)

    elif condition == "Use Caution":

        st.warning(condition)

    else:

        st.error(condition)

    st.write("**Weather Analysis:**")

    for reason in plan["summary_reasons"]:

        st.write("- " + reason)

    # ----------------------------------------------
    # SUITABLE ACTIVITIES
    # ----------------------------------------------

    st.divider()

    st.subheader("Suitable Activities")

    st.write(
        "Activities with a suitability score of 70 or above."
    )

    if len(plan["suitable_activities"]) > 0:

        display_activities(
            plan["suitable_activities"]
        )

    else:

        st.info(
            "No activities currently meet the suitable score."
        )

    # ----------------------------------------------
    # CAUTION ACTIVITIES
    # ----------------------------------------------

    st.divider()

    st.subheader("Activities Requiring Caution")

    st.write(
        "These activities may be possible, but "
        "weather conditions can affect comfort or safety."
    )

    if len(plan["caution_activities"]) > 0:

        display_activities(
            plan["caution_activities"]
        )

    else:

        st.info(
            "No activities were classified under caution."
        )

    # ----------------------------------------------
    # ACTIVITIES TO AVOID
    # ----------------------------------------------

    st.divider()

    st.subheader("Activities to Avoid")

    st.write(
        "Activities with a suitability score below 45."
    )

    if len(plan["activities_to_avoid"]) > 0:

        display_activities(
            plan["activities_to_avoid"]
        )

    else:

        st.success(
            "No activities were classified as unsuitable "
            "by the planner."
        )

    # ----------------------------------------------
    # SAFETY INFORMATION
    # ----------------------------------------------

    st.divider()

    st.subheader("Important Safety Information")

    st.info(
        "These recommendations are generated using "
        "weather-based rules and suitability scores. "
        "They are general guidance, not official safety "
        "clearance. Check local weather alerts, beach "
        "conditions, sea-state warnings and activity "
        "restrictions before going outdoors."
    )

    st.caption(
        "Suitability scores are rule-based estimates, "
        "not probabilities or machine-learning predictions."
    )


# --------------------------------------------------
# INITIAL PAGE MESSAGE
# --------------------------------------------------

elif "activity_plan" not in st.session_state:

    st.info(
        "Select a location and click "
        "'Generate Activity Suggestions' to begin."
    )

else:

    st.info(
        "Click 'Generate Activity Suggestions' "
        "to load results for the selected location."
    )

render_footer()

"""
File Name: app.py
Project: Goa Weather Prediction and Activity Planner

Purpose:
Main entry point of the Streamlit application.
Displays the home page, project overview, system workflow,
locations, navigation and machine learning model information.
"""

import streamlit as st

from config import (
    APP_TITLE,
    APP_ICON,
    PAGE_LAYOUT,
    LOCATIONS
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
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=PAGE_LAYOUT,
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# APPLY CUSTOM STYLE
# --------------------------------------------------

apply_custom_style()


# --------------------------------------------------
# HOME PAGE HEADER
# --------------------------------------------------

render_header(
    "Goa Weather Intelligence",
    "Weather Prediction and Outdoor Activity Planner"
)


# --------------------------------------------------
# INTRODUCTION
# --------------------------------------------------

st.markdown(
    """
    This application combines real-time weather information
    with a Machine Learning model to estimate temperature
    across different locations in Goa.

    It also evaluates current weather conditions to provide
    suitable outdoor and indoor activity suggestions.
    """
)

st.write("")


# --------------------------------------------------
# PROJECT OVERVIEW
# --------------------------------------------------

st.subheader("Project Overview")

st.caption(
    "An overview of the application's coverage and model performance."
)

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.metric(
            label="Locations Covered",
            value=len(LOCATIONS)
        )
        st.caption("Across Goa")

with col2:
    with st.container(border=True):
        st.metric(
            label="Prediction Algorithm",
            value="Batch GD"
        )
        st.caption("Linear Regression")

with col3:
    with st.container(border=True):
        st.metric(
            label="Model R² Score",
            value="0.7408"
        )
        st.caption("Held-out historical test data")


# --------------------------------------------------
# MODEL PERFORMANCE
# --------------------------------------------------

st.write("")

with st.container(border=True):

    st.markdown("**Model Performance**")

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric(
            label="MAE",
            value="1.4518 °C"
        )

    with metric2:
        st.metric(
            label="RMSE",
            value="1.8771 °C"
        )

    with metric3:
        st.metric(
            label="R² Score",
            value="0.7408"
        )

    st.caption(
        "These values represent performance on the held-out "
        "historical test dataset, not future forecast accuracy."
    )


# --------------------------------------------------
# SYSTEM WORKFLOW
# --------------------------------------------------

st.divider()

st.subheader("How the System Works")

st.caption(
    "The application follows four main processing stages."
)

workflow = [
    {
        "number": "01",
        "title": "Weather Data Collection",
        "description": (
            "Retrieves current weather information "
            "from the Open-Meteo Forecast API."
        )
    },
    {
        "number": "02",
        "title": "Data Preprocessing",
        "description": (
            "Prepares weather variables and time-based "
            "features in the format used during training."
        )
    },
    {
        "number": "03",
        "title": "Temperature Estimation",
        "description": (
            "Uses the trained Batch Gradient Descent "
            "model to estimate temperature."
        )
    },
    {
        "number": "04",
        "title": "Activity Planning",
        "description": (
            "Evaluates current weather conditions using "
            "rules to suggest suitable activities."
        )
    }
]

workflow_columns = st.columns(4)

for i in range(4):

    with workflow_columns[i]:

        with st.container(border=True):

            st.markdown(
                f"### {workflow[i]['number']}"
            )

            st.markdown(
                f"**{workflow[i]['title']}**"
            )

            st.caption(
                workflow[i]["description"]
            )


# --------------------------------------------------
# APPLICATION FEATURES
# --------------------------------------------------

st.divider()

st.subheader("Explore the Application")

st.caption(
    "Select a feature to access its functionality."
)

feature1, feature2 = st.columns(2)

with feature1:

    with st.container(border=True):

        st.markdown("### 🌤️ Weather Prediction")

        st.write(
            """
            View current weather information for a selected
            Goa location and estimate its temperature using
            the trained Machine Learning model.
            """
        )

        st.page_link(
            "pages/1_Weather_Prediction.py",
            label="Open Weather Prediction",
            icon="🌤️",
            use_container_width=True
        )


with feature2:

    with st.container(border=True):

        st.markdown("### 🌳 Activity Suggestions")

        st.write(
            """
            Explore outdoor and indoor activities based on
            current temperature, rainfall, humidity, wind,
            UV index and other weather conditions.
            """
        )

        st.page_link(
            "pages/2_Activity_Suggestions.py",
            label="Open Activity Suggestions",
            icon="🌳",
            use_container_width=True
        )


# --------------------------------------------------
# LOCATIONS COVERED
# --------------------------------------------------

st.divider()

st.subheader("Locations Covered")

st.caption(
    "The application supports weather information for "
    "the following ten locations in Goa."
)

location_names = list(LOCATIONS.keys())

location_columns = st.columns(5)

for i, location in enumerate(location_names):

    with location_columns[i % 5]:

        with st.container(border=True):

            st.markdown(
                f"**{location}**"
            )


# --------------------------------------------------
# MACHINE LEARNING MODEL INFORMATION
# --------------------------------------------------

st.divider()

st.subheader("Machine Learning Model")

with st.expander(
    "View Model Details",
    expanded=False
):

    model_col1, model_col2 = st.columns(2)

    with model_col1:

        st.markdown("**Training Configuration**")

        st.write("Algorithm: Batch Gradient Descent")

        st.write("Model: Linear Regression")

        st.write("Target Variable: `temperature_2m`")

        st.write("Training Iterations: 1000")

        st.write("Learning Rate: 0.01")


    with model_col2:

        st.markdown("**Input Features**")

        st.write(
            """
            1. Relative Humidity
            2. Precipitation
            3. Wind Speed
            4. Atmospheric Pressure
            5. Cyclical Hour Features
            6. Cyclical Month Features
            7. Latitude
            8. Longitude
            """
        )


# --------------------------------------------------
# DATA SOURCE AND PROJECT INFORMATION
# --------------------------------------------------

st.divider()

st.subheader("Data Source")

st.write(
    """
    Weather information is obtained from the
    Open-Meteo API. The temperature estimation model
    is trained using historical weather data and
    implemented using custom Batch Gradient Descent.
    """
)

st.caption(
    "Note: Activity suitability scores are based on "
    "rule-based weather evaluation. They are not ML "
    "predictions or guarantees of outdoor safety."
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

render_footer()

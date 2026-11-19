
"""
File Name: style.py
Project: Goa Weather Prediction and Activity Planner

Purpose:
Provides consistent styling, header, footer and
section components across all Streamlit pages.
"""

import streamlit as st


# --------------------------------------------------
# APPLY PROJECT THEME
# --------------------------------------------------

def apply_custom_style():

    st.html("""
    <style>

    /* =========================================
       1. GLOBAL DESIGN
    ========================================= */

    .stApp {
        background-color: #FFF7E5;
        color: #31241F;
        font-family: "Segoe UI", sans-serif;
    }

    .block-container {
        max-width: 1250px;
        padding: 2rem 2rem 2.5rem;
    }

    p, li, label {
        color: #31241F;
        line-height: 1.65;
    }


    /* =========================================
       2. SIDEBAR
    ========================================= */

    [data-testid="stSidebar"] {
        background-color: #75E6DA;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] a {
        color: #31241F !important;
    }


    /* =========================================
       3. HEADINGS
    ========================================= */

    h1, h2, h3, h4 {
        color: #31241F !important;
        font-weight: 700 !important;
    }

    h1 {
        font-size: 2.2rem !important;
    }

    h2 {
        font-size: 1.6rem !important;
    }

    h3 {
        font-size: 1.2rem !important;
    }


    /* =========================================
       4. PROJECT HEADER
    ========================================= */

    .project-header {
        background: linear-gradient(
            115deg,
            #EB110B,
            #C90E09
        );

        border-radius: 16px;
        padding: 35px 38px;
        margin-bottom: 28px;

        box-shadow: 0 6px 20px rgba(49, 36, 31, 0.12);
    }

    .header-label {
        color: #EB110B;
        background-color: #FFF7E5;

        display: inline-block;
        padding: 6px 13px;

        border-radius: 20px;

        font-size: 11px;
        font-weight: 750;
        letter-spacing: 1.5px;

        margin-bottom: 15px;
    }

    .project-header h1 {
        color: #FFFFFF !important;
        font-size: 36px !important;
        font-weight: 800 !important;

        margin: 0;
        padding: 0;
    }

    .project-header p {
        color: #FFF7E5 !important;
        font-size: 16px;

        margin-top: 10px;
        margin-bottom: 0;
    }


    /* =========================================
       5. SECTION HEADINGS
    ========================================= */

    .section-heading {
        color: #31241F;
        font-size: 22px;
        font-weight: 750;

        border-left: 5px solid #EB110B;
        padding-left: 13px;

        margin-top: 28px;
        margin-bottom: 18px;
    }


    /* =========================================
       6. METRIC CARDS
    ========================================= */

    [data-testid="stMetric"] {
        background-color: #FFFFFF;

        border: 1px solid #E9DCC5;
        border-left: 3px solid #EB110B;

        border-radius: 12px;
        padding: 17px;

        box-shadow: 0 3px 10px rgba(49, 36, 31, 0.05);
    }

    [data-testid="stMetricLabel"] {
        color: #66544C !important;
    }

    [data-testid="stMetricValue"] {
        color: #31241F !important;
        font-weight: 750;
    }


    /* =========================================
       7. CONTAINERS
    ========================================= */

    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF;
        border: 1px solid #E9DCC5;
        border-radius: 13px;
    }


    /* =========================================
       8. BUTTONS
    ========================================= */

    .stButton > button {
        background-color: #EB110B;
        color: #FFFFFF;

        border: 1px solid #EB110B;
        border-radius: 8px;

        padding: 9px 18px;
        font-weight: 650;

        transition: 0.2s ease;
    }

    .stButton > button:hover {
        background-color: #C90E09;
        border-color: #C90E09;
        color: #FFFFFF;
    }

    .stButton > button:focus {
        box-shadow: 0 0 0 2px #75E6DA;
    }


    /* =========================================
       9. PAGE LINKS
    ========================================= */

    [data-testid="stPageLink"] a {
        background-color: #EB110B;
        color: #FFFFFF !important;

        border-radius: 8px;
        font-weight: 600;
    }


    /* =========================================
       10. INPUTS
    ========================================= */

    [data-baseweb="select"] > div {
        border-radius: 8px;
    }

    [data-baseweb="input"],
    [data-baseweb="textarea"] {
        border-radius: 8px;
    }


    /* =========================================
       11. EXPANDERS
    ========================================= */

    [data-testid="stExpander"] {
        background-color: #FFFFFF;
        border: 1px solid #E9DCC5;
        border-radius: 10px;
    }


    /* =========================================
       12. ALERTS
    ========================================= */

    [data-testid="stAlert"] {
        border-radius: 10px;
    }


    /* =========================================
       13. PROGRESS BARS
    ========================================= */

    .stProgress > div > div > div > div {
        background-color: #EB110B;
    }


    /* =========================================
       14. DATA TABLES
    ========================================= */

    [data-testid="stDataFrame"],
    [data-testid="stTable"] {
        border: 1px solid #E9DCC5;
        border-radius: 10px;
        overflow: hidden;
    }


    /* =========================================
       15. DIVIDERS
    ========================================= */

    hr {
        border-color: #E9DCC5;
        margin: 1.5rem 0;
    }


    /* =========================================
       16. PROJECT FOOTER
    ========================================= */

    .project-footer {
        background-color: #31241F;

        border-radius: 13px;
        padding: 26px 20px;

        text-align: center;

        margin-top: 40px;
        margin-bottom: 10px;
    }

    .footer-title {
        color: #75E6DA !important;

        font-size: 15px;
        font-weight: 750;
        letter-spacing: 1.5px;

        margin-bottom: 10px;
    }

    .footer-description {
        color: #FFF7E5 !important;
        font-size: 13px;
        margin: 5px 0;
    }

    .footer-subtitle {
        color: #C9BDB2 !important;
        font-size: 11px;
        margin-top: 9px;
    }


    /* =========================================
       17. RESPONSIVE DESIGN
    ========================================= */

    @media (max-width: 768px) {

        .block-container {
            padding: 1rem;
        }

        .project-header {
            padding: 25px 22px;
        }

        .project-header h1 {
            font-size: 26px !important;
        }

        .project-header p {
            font-size: 14px;
        }

    }

    </style>
    """)


# --------------------------------------------------
# PROJECT HEADER
# --------------------------------------------------

def render_header(
    page_title="Goa Weather Intelligence",
    page_description="Weather Prediction and Outdoor Activity Planner"
):

    st.html(f"""
    <div class="project-header">

        <div class="header-label">
            GOA WEATHER INTELLIGENCE
        </div>

        <h1>{page_title}</h1>

        <p>{page_description}</p>

    </div>
    """)


# --------------------------------------------------
# SECTION HEADING
# --------------------------------------------------

def render_section_heading(title):

    st.html(f"""
    <div class="section-heading">
        {title}
    </div>
    """)


# --------------------------------------------------
# PROJECT FOOTER
# --------------------------------------------------

def render_footer():

    st.html("""
    <div class="project-footer">

        <div class="footer-title">
            GOA WEATHER INTELLIGENCE
        </div>

        <p class="footer-description">
            Weather Prediction and Outdoor Activity Planner
        </p>

        <p class="footer-subtitle">
            Powered by Open-Meteo API and Batch Gradient Descent
        </p>

        <p class="footer-subtitle">
            Academic Mini Project | 2026
        </p>

    </div>
    """)

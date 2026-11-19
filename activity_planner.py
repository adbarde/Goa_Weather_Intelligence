
"""
File Name: activity_planner.py
Project: Goa Weather Prediction and Activity Planner

Purpose:
Evaluates weather conditions and generates
explainable activity recommendations.
"""


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def get_number(value, default=None):

    """
    Safely converts a value into a number.
    Handles None, NaN and invalid values.
    """

    try:

        if value is None:
            return default

        number = float(value)

        if number != number:
            return default

        return number

    except (TypeError, ValueError):

        return default


def is_thunderstorm(weather_code):

    """
    Checks whether the weather code represents
    a thunderstorm.
    """

    code = get_number(weather_code)

    return code is not None and int(code) in [95, 96, 99]


# --------------------------------------------------
# TEMPERATURE CLASSIFICATION
# --------------------------------------------------

def classify_temperature(temperature):

    if temperature < 15:
        return "Cold"

    elif temperature < 25:
        return "Pleasant"

    elif temperature < 34:
        return "Warm"

    else:
        return "Hot"


# --------------------------------------------------
# WEATHER CONDITION DESCRIPTION
# --------------------------------------------------

def get_weather_description(weather_code):

    code = get_number(weather_code)

    if code is None:
        return "Weather condition unavailable"

    code = int(code)

    if code == 0:
        return "Clear sky"

    elif code in [1, 2]:
        return "Mainly clear or partly cloudy"

    elif code == 3:
        return "Overcast"

    elif code in [45, 48]:
        return "Foggy conditions"

    elif code in [51, 53, 55]:
        return "Drizzle"

    elif code in [56, 57]:
        return "Freezing drizzle"

    elif code in [61, 63, 65]:
        return "Rain"

    elif code in [66, 67]:
        return "Freezing rain"

    elif code in [71, 73, 75, 77]:
        return "Snow conditions"

    elif code in [80, 81, 82]:
        return "Rain showers"

    elif code in [85, 86]:
        return "Snow showers"

    elif code in [95, 96, 99]:
        return "Thunderstorm"

    else:
        return "Variable weather conditions"


# --------------------------------------------------
# ACTIVITY DATABASE
# --------------------------------------------------

def get_activities():

    """
    Defines activities and their weather sensitivity.
    """

    activities = [

        {
            "name": "Outdoor Walking",
            "outdoor": True,
            "strenuous": False,
            "sun_exposure": True,
            "wind_sensitive": False
        },

        {
            "name": "Jogging and Running",
            "outdoor": True,
            "strenuous": True,
            "sun_exposure": True,
            "wind_sensitive": False
        },

        {
            "name": "Cycling",
            "outdoor": True,
            "strenuous": True,
            "sun_exposure": True,
            "wind_sensitive": True
        },

        {
            "name": "Beach Visit and Beach Walk",
            "outdoor": True,
            "strenuous": False,
            "sun_exposure": True,
            "wind_sensitive": True
        },

        {
            "name": "Nature Photography",
            "outdoor": True,
            "strenuous": False,
            "sun_exposure": True,
            "wind_sensitive": False
        },

        {
            "name": "Outdoor Sports",
            "outdoor": True,
            "strenuous": True,
            "sun_exposure": True,
            "wind_sensitive": True
        },

        {
            "name": "Heritage Sightseeing",
            "outdoor": True,
            "strenuous": False,
            "sun_exposure": True,
            "wind_sensitive": False
        },

        {
            "name": "Indoor Sightseeing",
            "outdoor": False,
            "strenuous": False,
            "sun_exposure": False,
            "wind_sensitive": False
        },

        {
            "name": "Indoor Games and Entertainment",
            "outdoor": False,
            "strenuous": False,
            "sun_exposure": False,
            "wind_sensitive": False
        },

        {
            "name": "Cafes and Indoor Leisure",
            "outdoor": False,
            "strenuous": False,
            "sun_exposure": False,
            "wind_sensitive": False
        }

    ]

    return activities


# --------------------------------------------------
# CALCULATE ACTIVITY SUITABILITY
# --------------------------------------------------

def evaluate_activity(
    activity,
    temperature,
    feels_like,
    humidity,
    precipitation,
    precipitation_probability,
    wind_speed,
    wind_gusts,
    uv_index,
    visibility,
    weather_code
):

    score = 100

    reasons = []

    outdoor = activity["outdoor"]

    strenuous = activity["strenuous"]

    sun_exposure = activity["sun_exposure"]

    wind_sensitive = activity["wind_sensitive"]

    thunderstorm = is_thunderstorm(weather_code)

    # ----------------------------------------------
    # TEMPERATURE CONDITIONS
    # ----------------------------------------------

    if outdoor:

        if feels_like >= 35:

            score -= 30

            reasons.append(
                "High apparent temperature may increase "
                "heat stress during outdoor activities."
            )

        elif feels_like >= 32:

            score -= 15

            reasons.append(
                "Warm conditions may make prolonged "
                "outdoor activity uncomfortable."
            )

        elif feels_like < 18:

            reasons.append(
                "Cooler conditions may require "
                "appropriate clothing."
            )

    # ----------------------------------------------
    # HUMIDITY CONDITIONS
    # ----------------------------------------------

    if outdoor and humidity is not None:

        if humidity >= 90:

            score -= 20

            reasons.append(
                "Very high humidity may reduce comfort "
                "and increase heat stress."
            )

        elif humidity >= 80:

            if strenuous:
                score -= 20
            else:
                score -= 10

            reasons.append(
                "High humidity may make outdoor "
                "activities feel more uncomfortable."
            )

    # ----------------------------------------------
    # RAINFALL CONDITIONS
    # ----------------------------------------------

    if outdoor:

        if precipitation is not None:

            if precipitation >= 5:

                score -= 40

                reasons.append(
                    "Significant precipitation is reported. "
                    "Outdoor activities may be disrupted."
                )

            elif precipitation > 0:

                score -= 25

                reasons.append(
                    "Precipitation is currently reported, "
                    "which may make outdoor surfaces wet."
                )

        if precipitation_probability is not None:

            if precipitation_probability >= 75:

                score -= 20

                reasons.append(
                    "High probability of precipitation "
                    "in the current forecast hour."
                )

            elif precipitation_probability >= 50:

                score -= 10

                reasons.append(
                    "There is a moderate chance of rain."
                )

    # ----------------------------------------------
    # WIND CONDITIONS
    # ----------------------------------------------

    if outdoor and wind_speed is not None:

        if wind_speed >= 40:

            score -= 25

            reasons.append(
                "Strong wind may make outdoor activities "
                "difficult or unsafe."
            )

        elif wind_speed >= 30:

            score -= 15

            reasons.append(
                "Windy conditions may affect outdoor comfort."
            )

        elif wind_speed >= 20 and wind_sensitive:

            score -= 10

            reasons.append(
                "Wind may affect cycling and other "
                "wind-sensitive activities."
            )

    if outdoor and wind_gusts is not None:

        if wind_gusts >= 40:

            score -= 20

            reasons.append(
                "Strong wind gusts may affect outdoor safety."
            )

    # ----------------------------------------------
    # UV INDEX CONDITIONS
    # ----------------------------------------------

    if outdoor and sun_exposure and uv_index is not None:

        if uv_index >= 8:

            score -= 25

            reasons.append(
                "Very high UV exposure. "
                "Sun protection and reduced exposure are advised."
            )

        elif uv_index >= 6:

            score -= 15

            reasons.append(
                "High UV exposure. "
                "Use sunscreen, protective clothing and shade."
            )

        elif uv_index >= 3:

            score -= 5

            reasons.append(
                "Sun protection is advisable."
            )

    # ----------------------------------------------
    # VISIBILITY CONDITIONS
    # ----------------------------------------------

    if outdoor and visibility is not None:

        if visibility < 1000:

            score -= 30

            reasons.append(
                "Very low visibility may affect outdoor "
                "movement and sightseeing."
            )

        elif visibility < 3000:

            score -= 15

            reasons.append(
                "Reduced visibility may affect sightseeing."
            )

    # ----------------------------------------------
    # THUNDERSTORM CONDITIONS
    # ----------------------------------------------

    if outdoor and thunderstorm:

        score -= 60

        reasons.append(
            "Thunderstorm conditions are reported. "
            "Avoid exposed outdoor activities."
        )

    # ----------------------------------------------
    # INDOOR ACTIVITY BENEFITS
    # ----------------------------------------------

    if not outdoor:

        if feels_like >= 32:

            score += 5

            reasons.append(
                "Indoor activities provide an alternative "
                "during hot weather."
            )

        if precipitation is not None and precipitation > 0:

            score += 10

            reasons.append(
                "Indoor activities are less affected "
                "by rainfall."
            )

        if thunderstorm:

            score += 10

            reasons.append(
                "Indoor activities avoid exposure "
                "to thunderstorms."
            )

    # ----------------------------------------------
    # FINAL SCORE
    # ----------------------------------------------
    
    score = max(0, min(100, score))

    if score >= 70:

        status = "Suitable"

    elif score >= 45:

        status = "Use Caution"

    else:

        status = "Avoid"

    if len(reasons) == 0:

        reasons.append(
            "Weather conditions are generally favourable."
        )

    return {

        "name": activity["name"],

        "score": int(score),

        "status": status,

        "reasons": reasons

    }

# --------------------------------------------------
# GENERATE ACTIVITY PLAN
# --------------------------------------------------

def generate_activity_plan(
    predicted_temperature,
    humidity,
    precipitation,
    wind_speed,
    apparent_temperature=None,
    precipitation_probability=None,
    wind_gusts=None,
    uv_index=None,
    visibility=None,
    cloud_cover=None,
    weather_code=None
):

    """
    Generates explainable activity recommendations
    using weather conditions.
    """

    # ----------------------------------------------
    # CONVERT INPUT VALUES SAFELY
    # ----------------------------------------------

    temperature = get_number(predicted_temperature, 30)

    humidity = get_number(humidity)

    precipitation = get_number(precipitation)

    wind_speed = get_number(wind_speed)

    apparent_temperature = get_number(apparent_temperature)

    precipitation_probability = get_number(
        precipitation_probability
    )

    wind_gusts = get_number(wind_gusts)

    uv_index = get_number(uv_index)

    visibility = get_number(visibility)

    cloud_cover = get_number(cloud_cover)

    weather_code = get_number(weather_code)

    # ----------------------------------------------
    # USE APPARENT TEMPERATURE WHEN AVAILABLE
    # ----------------------------------------------

    if apparent_temperature is not None:

        feels_like = apparent_temperature

    else:

        feels_like = temperature

    # ----------------------------------------------
    # EVALUATE ALL ACTIVITIES
    # ----------------------------------------------

    activities = get_activities()

    results = []

    for activity in activities:

        result = evaluate_activity(

            activity,

            temperature,

            feels_like,

            humidity,

            precipitation,

            precipitation_probability,

            wind_speed,

            wind_gusts,

            uv_index,

            visibility,

            weather_code

        )

        results.append(result)

    # ----------------------------------------------
    # SORT BY SUITABILITY SCORE
    # ----------------------------------------------

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    # ----------------------------------------------
    # SEPARATE ACTIVITIES BY STATUS
    # ----------------------------------------------

    suitable_activities = []

    caution_activities = []

    activities_to_avoid = []

    for result in results:

        if result["status"] == "Suitable":

            suitable_activities.append(result)

        elif result["status"] == "Use Caution":

            caution_activities.append(result)

        else:

            activities_to_avoid.append(result)

    # ----------------------------------------------
    # OVERALL WEATHER CONDITION
    # ----------------------------------------------

    thunderstorm = is_thunderstorm(weather_code)

    if (

        thunderstorm

        or (
            precipitation is not None
            and precipitation >= 5
        )

        or (
            wind_speed is not None
            and wind_speed >= 40
        )

    ):

        overall_condition = "Unfavourable for outdoor activities"

    elif (

        feels_like >= 35

        or (
            humidity is not None
            and humidity >= 85
        )

        or (
            precipitation is not None
            and precipitation > 0
        )

        or (
            wind_speed is not None
            and wind_speed >= 30
        )

        or (
            uv_index is not None
            and uv_index >= 8
        )

    ):

        overall_condition = "Use Caution"

    else:

        overall_condition = "Generally Favourable"

    # ----------------------------------------------
    # GENERAL WEATHER EXPLANATIONS
    # ----------------------------------------------

    summary_reasons = []

    if feels_like >= 35:

        summary_reasons.append(
            "High apparent temperature: prefer indoor "
            "activities or cooler hours."
        )

    elif feels_like >= 32:

        summary_reasons.append(
            "Warm conditions: avoid prolonged strenuous "
            "outdoor activity."
        )

    if humidity is not None and humidity >= 85:

        summary_reasons.append(
            "High humidity may increase discomfort."
        )

    if precipitation is not None and precipitation > 0:

        summary_reasons.append(
            "Rainfall is reported. Check conditions "
            "before planning outdoor activities."
        )

    if (
        precipitation_probability is not None
        and precipitation_probability >= 50
    ):

        summary_reasons.append(
            "The forecast indicates a chance of rain."
        )

    if wind_speed is not None and wind_speed >= 30:

        summary_reasons.append(
            "Strong wind may affect outdoor activities."
        )

    if uv_index is not None and uv_index >= 6:

        summary_reasons.append(
            "High UV exposure requires sun protection."
        )

    if thunderstorm:

        summary_reasons.append(
            "Thunderstorm conditions are reported. "
            "Avoid exposed outdoor activities."
        )

    if len(summary_reasons) == 0:

        summary_reasons.append(
            "No major weather-related restriction "
            "was identified by the planner."
        )

    # ----------------------------------------------
    # RETURN RESULTS
    # ----------------------------------------------

    return {

        "temperature_condition":
            classify_temperature(feels_like),

        "overall_condition":
            overall_condition,

        "weather_description":
            get_weather_description(weather_code),

        "feels_like":
            feels_like,

        "suitable_activities":
            suitable_activities,

        "caution_activities":
            caution_activities,

        "activities_to_avoid":
            activities_to_avoid,

        "summary_reasons":
            summary_reasons,

        "weather_details": {

            "temperature": temperature,

            "apparent_temperature": feels_like,

            "humidity": humidity,

            "precipitation": precipitation,

            "precipitation_probability":
                precipitation_probability,

            "wind_speed": wind_speed,

            "wind_gusts": wind_gusts,

            "uv_index": uv_index,

            "cloud_cover": cloud_cover,

            "visibility": visibility

        }

    }


# --------------------------------------------------
# TEST ACTIVITY PLANNER
# --------------------------------------------------

if __name__ == "__main__":

    plan = generate_activity_plan(

        predicted_temperature=30,

        humidity=75,

        precipitation=0,

        wind_speed=15,

        apparent_temperature=33,

        precipitation_probability=10,

        wind_gusts=20,

        uv_index=7,

        visibility=10000,

        cloud_cover=30,

        weather_code=1

    )

    print("\nACTIVITY PLANNER RESULTS")

    print("------------------------")

    print("\nOverall Condition:")

    print(plan["overall_condition"])

    print("\nTemperature Condition:")

    print(plan["temperature_condition"])

    print("\nWeather Description:")

    print(plan["weather_description"])

    print("\nSuitable Activities:")

    for activity in plan["suitable_activities"]:

        print(
            activity["name"],
            "-",
            activity["score"],
            "/100"
        )

        for reason in activity["reasons"]:

            print("  Reason:", reason)

    print("\nActivities Requiring Caution:")

    for activity in plan["caution_activities"]:

        print(
            activity["name"],
            "-",
            activity["score"],
            "/100"
        )

        for reason in activity["reasons"]:

            print("  Reason:", reason)

    print("\nActivities to Avoid:")

    for activity in plan["activities_to_avoid"]:

        print(
            activity["name"],
            "-",
            activity["score"],
            "/100"
        )

        for reason in activity["reasons"]:

            print("  Reason:", reason)

    print("\nGeneral Weather Explanations:")

    for reason in plan["summary_reasons"]:

        print("-", reason)

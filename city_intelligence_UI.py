from dotenv import load_dotenv
load_dotenv()

import os
import time
import requests
import streamlit as st

from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from tavily import TavilyClient
from langchain.agents import create_agent


# =========================================================
# STREAMLIT CONFIG
# =========================================================

st.set_page_config(
    page_title="AI City Intelligence",
    page_icon="🌍",
    layout="wide"
)


# =========================================================
# WEATHER TOOL
# =========================================================

API_KEY = os.getenv("OPENWEATHER_API_KEY")


@tool
def get_weather(city: str) -> str:
    """Get current weather information for a city."""

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )
    except requests.exceptions.RequestException:
        return f"Could not connect to weather service for {city}."

    if response.status_code != 200:
        return f"Could not get weather information for {city}."

    data = response.json()

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    return (
        f"Weather in {city}: "
        f"{desc}, "
        f"Temperature: {temp}°C"
    )


# =========================================================
# AIR QUALITY TOOL
# =========================================================

@tool
def get_air_quality(city: str) -> str:
    """Get current air quality information for a city."""

    api_key = os.getenv("OPENWEATHER_API_KEY")

    geocode_url = (
        "https://api.openweathermap.org/geo/1.0/direct"
    )

    geocode_params = {
        "q": city,
        "limit": 1,
        "appid": api_key
    }

    try:
        response = requests.get(
            geocode_url,
            params=geocode_params,
            timeout=10
        )
    except requests.exceptions.RequestException:
        return f"Could not connect to location service for {city}."

    if response.status_code != 200:
        return f"Could not find location for {city}."

    data = response.json()

    if not data:
        return f"Could not find location for {city}."

    lat = data[0]["lat"]
    lon = data[0]["lon"]

    air_url = (
        "https://api.openweathermap.org/data/2.5/air_pollution"
    )

    air_params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key
    }

    try:
        response = requests.get(
            air_url,
            params=air_params,
            timeout=10
        )
    except requests.exceptions.RequestException:
        return f"Could not get air quality for {city}."

    if response.status_code != 200:
        return f"Could not get air quality for {city}."

    data = response.json()

    air_data = data.get("list", [])

    if not air_data:
        return f"No air quality data found for {city}."

    current = air_data[0]

    aqi = current["main"]["aqi"]
    components = current["components"]

    pm25 = components.get("pm2_5", 0)
    pm10 = components.get("pm10", 0)
    co = components.get("co", 0)
    no2 = components.get("no2", 0)
    o3 = components.get("o3", 0)

    aqi_levels = {
        1: "Good",
        2: "Fair",
        3: "Moderate",
        4: "Poor",
        5: "Very Poor"
    }

    aqi_text = aqi_levels.get(
        aqi,
        "Unknown"
    )

    return (
        f"Air Quality in {city}\n"
        f"AQI: {aqi} ({aqi_text})\n"
        f"PM2.5: {pm25:.2f} μg/m³\n"
        f"PM10: {pm10:.2f} μg/m³\n"
        f"CO: {co:.2f} μg/m³\n"
        f"NO₂: {no2:.2f} μg/m³\n"
        f"O₃: {o3:.2f} μg/m³"
    )


# =========================================================
# NEWS TOOL
# =========================================================

tavily_client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


@tool
def get_news(city: str) -> str:
    """Get the latest news about a city."""

    try:
        response = tavily_client.search(
            query=f"latest news about {city}",
            search_depth="basic",
            max_results=3
        )
    except Exception as e:
        return f"Could not get news for {city}: {e}"

    results = response.get("results", [])

    if not results:
        return f"No news found for {city}."

    news = []

    for result in results:

        title = result.get(
            "title",
            "Untitled"
        )

        content = result.get(
            "content",
            "No content available."
        )

        url = result.get(
            "url",
            ""
        )

        news.append(
            f"Title: {title}\n"
            f"Content: {content}\n"
            f"URL: {url}"
        )

    return "\n\n".join(news)


# =========================================================
# PLACES TOOL
# =========================================================

@tool
def get_places(city: str) -> str:
    """Find interesting places to visit in a city."""

    api_key = os.getenv("GEOAPIFY_API_KEY")

    geocode_url = (
        "https://api.geoapify.com/v1/geocode/search"
    )

    geocode_params = {
        "text": city,
        "apiKey": api_key,
        "limit": 1
    }

    try:
        response = requests.get(
            geocode_url,
            params=geocode_params,
            timeout=10
        )
    except requests.exceptions.RequestException:
        return f"Could not connect to Geoapify for {city}."

    if response.status_code != 200:
        return f"Could not find location for {city}."

    data = response.json()

    features = data.get(
        "features",
        []
    )

    if not features:
        return f"Could not find location for {city}."

    coordinates = features[0]["geometry"]["coordinates"]

    lon = coordinates[0]
    lat = coordinates[1]

    places_url = (
        "https://api.geoapify.com/v2/places"
    )

    places_params = {
        "categories": "tourism.sights,entertainment",
        "filter": f"circle:{lon},{lat},10000",
        "limit": 10,
        "apiKey": api_key
    }

    try:
        response = requests.get(
            places_url,
            params=places_params,
            timeout=10
        )
    except requests.exceptions.RequestException:
        return f"Could not get places in {city}."

    if response.status_code != 200:
        return f"Could not find places in {city}."

    data = response.json()

    places = data.get(
        "features",
        []
    )

    if not places:
        return f"No interesting places found in {city}."

    results = []

    for i, place in enumerate(
        places,
        start=1
    ):

        properties = place.get(
            "properties",
            {}
        )

        name = properties.get(
            "name"
        ) or "Unknown place"

        address = properties.get(
            "formatted"
        ) or "Address not available"

        results.append(
            f"{i}. {name}\n"
            f"   Address: {address}"
        )

    return "\n\n".join(results)


# =========================================================
# RESTAURANTS TOOL
# =========================================================

@tool
def get_restaurants(city: str) -> str:
    """Find restaurants in a city."""

    api_key = os.getenv("GEOAPIFY_API_KEY")

    geocode_url = (
        "https://api.geoapify.com/v1/geocode/search"
    )

    geocode_params = {
        "text": city,
        "apiKey": api_key,
        "limit": 1
    }

    try:
        response = requests.get(
            geocode_url,
            params=geocode_params,
            timeout=10
        )
    except requests.exceptions.RequestException:
        return f"Could not connect to Geoapify for {city}."

    if response.status_code != 200:
        return f"Could not find location for {city}."

    data = response.json()

    features = data.get(
        "features",
        []
    )

    if not features:
        return f"Could not find location for {city}."

    coordinates = features[0]["geometry"]["coordinates"]

    lon = coordinates[0]
    lat = coordinates[1]

    restaurants_url = (
        "https://api.geoapify.com/v2/places"
    )

    restaurants_params = {
        "categories": "catering.restaurant",
        "filter": f"circle:{lon},{lat},10000",
        "limit": 10,
        "apiKey": api_key
    }

    try:
        response = requests.get(
            restaurants_url,
            params=restaurants_params,
            timeout=10
        )
    except requests.exceptions.RequestException:
        return f"Could not get restaurants in {city}."

    if response.status_code != 200:
        return f"Could not find restaurants in {city}."

    data = response.json()

    restaurants = data.get(
        "features",
        []
    )

    if not restaurants:
        return f"No restaurants found in {city}."

    results = []

    for i, restaurant in enumerate(
        restaurants,
        start=1
    ):

        properties = restaurant.get(
            "properties",
            {}
        )

        name = properties.get(
            "name"
        ) or "Unknown restaurant"

        address = properties.get(
            "formatted"
        ) or "Address not available"

        results.append(
            f"{i}. {name}\n"
            f"   Address: {address}"
        )

    return "\n\n".join(results)


# =========================================================
# DIRECTIONS TOOL
# =========================================================

@tool
def get_directions(
    source: str,
    destination: str
) -> str:
    """Find driving directions between two locations."""

    api_key = os.getenv("GEOAPIFY_API_KEY")

    geocode_url = (
        "https://api.geoapify.com/v1/geocode/search"
    )

    # -----------------------------------------
    # Source
    # -----------------------------------------

    source_params = {
        "text": source,
        "apiKey": api_key,
        "limit": 1
    }

    try:
        response = requests.get(
            geocode_url,
            params=source_params,
            timeout=10
        )
    except requests.exceptions.RequestException:
        return f"Could not find location: {source}"

    if response.status_code != 200:
        return f"Could not find location: {source}"

    data = response.json()

    features = data.get(
        "features",
        []
    )

    if not features:
        return f"Could not find location: {source}"

    source_coordinates = (
        features[0]["geometry"]["coordinates"]
    )

    source_lon = source_coordinates[0]
    source_lat = source_coordinates[1]

    # -----------------------------------------
    # Destination
    # -----------------------------------------

    destination_params = {
        "text": destination,
        "apiKey": api_key,
        "limit": 1
    }

    try:
        response = requests.get(
            geocode_url,
            params=destination_params,
            timeout=10
        )
    except requests.exceptions.RequestException:
        return f"Could not find location: {destination}"

    if response.status_code != 200:
        return f"Could not find location: {destination}"

    data = response.json()

    features = data.get(
        "features",
        []
    )

    if not features:
        return f"Could not find location: {destination}"

    destination_coordinates = (
        features[0]["geometry"]["coordinates"]
    )

    destination_lon = destination_coordinates[0]
    destination_lat = destination_coordinates[1]

    # -----------------------------------------
    # Routing
    # -----------------------------------------

    routing_url = (
        "https://api.geoapify.com/v1/routing"
    )

    waypoints = (
        f"{source_lat},{source_lon}|"
        f"{destination_lat},{destination_lon}"
    )

    routing_params = {
        "waypoints": waypoints,
        "mode": "drive",
        "format": "json",
        "units": "metric",
        "apiKey": api_key
    }

    try:
        response = requests.get(
            routing_url,
            params=routing_params,
            timeout=10
        )
    except requests.exceptions.RequestException:
        return "Could not calculate the route."

    if response.status_code != 200:
        return "Could not calculate the route."

    data = response.json()

    routes = data.get(
        "results",
        []
    )

    if not routes:
        return "No route found."

    route = routes[0]

    distance_km = (
        route.get("distance", 0) / 1000
    )

    time_minutes = (
        route.get("time", 0) / 60
    )

    toll = route.get(
        "toll",
        False
    )

    toll_text = (
        "Yes"
        if toll
        else "No"
    )

    return (
        f"Route from {source} to {destination}\n"
        f"Distance: {distance_km:.2f} km\n"
        f"Estimated time: {time_minutes:.0f} minutes\n"
        f"Tolls: {toll_text}"
    )


# =========================================================
# HOTELS TOOL
# =========================================================

@tool
def get_hotels(city: str) -> str:
    """Find hotels in a city."""

    api_key = os.getenv("STAYING_API_KEY")

    url = (
        "https://api.stayingapi.com/v1/search"
    )

    params = {
        "location": city,
        "checkIn": "2026-10-10",
        "checkOut": "2026-10-11",
        "adults": 2,
        "children": 0,
        "platforms": "google"
    }

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    # -----------------------------------------
    # Start search
    # -----------------------------------------

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=30
        )
    except requests.exceptions.RequestException as e:
        return f"Hotel API request failed: {e}"

    # -----------------------------------------
    # Search completed
    # -----------------------------------------

    if response.status_code == 200:

        data = response.json()

        hotels = data.get(
            "data",
            []
        )

    # -----------------------------------------
    # Async search
    # -----------------------------------------

    elif response.status_code == 202:

        data = response.json()

        job_id = (
            data.get("data", {})
            .get("jobId")
        )

        if not job_id:
            return (
                "Hotel search started "
                "but no job ID was returned."
            )

        job_url = (
            f"https://api.stayingapi.com/"
            f"v1/jobs/{job_id}"
        )

        hotels = []

        for attempt in range(12):

            time.sleep(5)

            try:
                job_response = requests.get(
                    job_url,
                    headers=headers,
                    timeout=30
                )
            except requests.exceptions.RequestException as e:
                return (
                    f"Could not check hotel search: {e}"
                )

            if job_response.status_code != 200:
                return (
                    "Could not check hotel "
                    f"search status: "
                    f"{job_response.status_code}"
                )

            job_data = job_response.json()

            job_info = (
                job_data.get("data")
                or {}
            )

            status = job_info.get(
                "status"
            )

            if status == "completed":

                hotels = job_info.get(
                    "result",
                    []
                )

                if isinstance(
                    hotels,
                    dict
                ):

                    hotels = (
                        hotels.get("data")
                        or hotels.get("results")
                        or []
                    )

                break

            if status == "failed":
                return "Hotel search failed."

        else:
            return (
                "Hotel search is taking too long. "
                "Please try again."
            )

    else:

        return (
            f"Hotel API error: "
            f"{response.status_code}\n"
            f"{response.text}"
        )

    # -----------------------------------------
    # No hotels
    # -----------------------------------------

    if not hotels:
        return f"No hotels found in {city}."

    # -----------------------------------------
    # Format hotels
    # -----------------------------------------

    results = []

    for i, hotel in enumerate(
        hotels[:10],
        start=1
    ):

        hotel = hotel or {}

        name = (
            hotel.get("name")
            or "Unknown hotel"
        )

        location = (
            hotel.get("location")
            or {}
        )

        hotel_city = (
            location.get("city")
            or city
        )

        star_rating = (
            hotel.get("starRating")
            if hotel.get("starRating") is not None
            else "N/A"
        )

        guest_rating = (
            hotel.get("guestRating")
            if hotel.get("guestRating") is not None
            else "N/A"
        )

        review_count = (
            hotel.get("reviewCount")
            if hotel.get("reviewCount") is not None
            else "N/A"
        )

        price = (
            hotel.get("price")
            or {}
        )

        nightly_price = (
            price.get("nightlyPrice")
            if price.get("nightlyPrice") is not None
            else "N/A"
        )

        currency = (
            price.get("currency")
            or ""
        )

        results.append(
            f"{i}. {name}\n"
            f"   City: {hotel_city}\n"
            f"   ⭐ Stars: {star_rating}\n"
            f"   👤 Guest Rating: {guest_rating}\n"
            f"   Reviews: {review_count}\n"
            f"   Price/night: "
            f"{nightly_price} {currency}"
        )

    return "\n\n".join(results)


# =========================================================
# CURRENCY TOOL
# =========================================================

@tool
def get_currency(
    amount: float,
    from_currency: str,
    to_currency: str
) -> str:
    """Convert an amount from one currency to another."""

    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    url = (
        f"https://api.frankfurter.dev/v2/rate/"
        f"{from_currency}/{to_currency}"
    )

    try:
        response = requests.get(
            url,
            timeout=10
        )
    except requests.exceptions.RequestException:
        return "Could not connect to currency service."

    if response.status_code != 200:
        return (
            f"Could not convert "
            f"{from_currency} to {to_currency}."
        )

    data = response.json()

    rate = data.get("rate")

    if rate is None:
        return "Exchange rate not available."

    converted_amount = (
        amount * rate
    )

    return (
        f"{amount:.2f} {from_currency} = "
        f"{converted_amount:.2f} {to_currency}\n"
        f"Exchange rate: 1 {from_currency} = "
        f"{rate:.4f} {to_currency}"
    )


# =========================================================
# LLM
# =========================================================

llm = ChatMistralAI(
    model="ministral-3b-2512"
)


# =========================================================
# AGENT
# =========================================================

agent = create_agent(
    llm,
    tools=[
        get_weather,
        get_air_quality,
        get_news,
        get_places,
        get_restaurants,
        get_directions,
        get_hotels,
        get_currency
    ],
    system_prompt="""
    You are an AI City Intelligence and Travel Assistant.

    You can help users with:

    - Weather
    - Air quality
    - Latest city news
    - Tourist places
    - Restaurants
    - Directions
    - Hotels
    - Currency conversion

    Select the appropriate tool based on the user's request.

    Use multiple tools when necessary.

    For example, if the user asks:
    "Plan a trip to Jaipur"

    you can use multiple tools to get:
    - Weather
    - Tourist places
    - Restaurants
    - Hotels

    Provide clear, concise and useful answers.

    Do not make up real-time information.
    Use the available tools whenever current information
    is required.
    """
)


# =========================================================
# STREAMLIT UI
# =========================================================

st.title("🌍 AI City Intelligence")

st.write(
    "Your AI-powered travel and city assistant"
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("🛠️ Available Tools")

    st.write("🌤️ Weather")
    st.write("🌫️ Air Quality")
    st.write("📰 Latest News")
    st.write("📍 Tourist Places")
    st.write("🍴 Restaurants")
    st.write("🗺️ Directions")
    st.write("🏨 Hotels")
    st.write("💱 Currency")

    st.divider()

    st.subheader("💡 Try asking")

    st.caption(
        "What is the weather in Jaipur?"
    )

    st.caption(
        "Find restaurants in Delhi."
    )

    st.caption(
        "What places should I visit in Mumbai?"
    )

    st.caption(
        "Find hotels in Jaipur."
    )

    st.caption(
        "Give directions from Bhopal to Delhi."
    )

    st.caption(
        "Convert 100 USD to INR."
    )

    st.divider()

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# =========================================================
# CHAT HISTORY
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# =========================================================
# WELCOME
# =========================================================

if not st.session_state.messages:

    st.info(
        "👋 Hello! Ask me anything about a city, "
        "travel, weather, restaurants, hotels, "
        "directions or currency."
    )


# =========================================================
# DISPLAY PREVIOUS MESSAGES
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# =========================================================
# USER INPUT
# =========================================================

user_input = st.chat_input(
    "Ask about any city..."
)


# =========================================================
# HANDLE USER MESSAGE
# =========================================================

if user_input:

    # Show user message

    with st.chat_message("user"):

        st.markdown(user_input)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # -----------------------------------------
    # Agent response
    # -----------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "🤖 Checking information..."
        ):

            try:

                result = agent.invoke(
                    {
                        "messages": [
                            {
                                "role": "user",
                                "content": user_input
                            }
                        ]
                    }
                )

                answer = (
                    result["messages"][-1]
                    .content
                )

            except Exception as e:

                answer = (
                    "❌ Something went wrong.\n\n"
                    f"Error: {str(e)}"
                )

            st.markdown(answer)

    # Save assistant response

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
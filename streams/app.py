import streamlit as st
import sys
import os

# Add parent folder to sys.path to import agents
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agents.news_aggregator import get_latest_weather_news
from agents.weather_data_collector import get_live_weather
from agents.fact_checker import fact_check_claim

st.set_page_config(page_title="verifly - Weather News Fact Checker", layout="wide")

# Header layout: verifly top-left, centered "Weather Fact Checking"
header_row = st.columns([8, 3])
with header_row[0]:
    st.markdown(
        "<h1 style='text-align: left; font-weight: 900; font-size: 52px; margin-bottom: 5px;'>verifly</h1>",
        unsafe_allow_html=True,
    )
with header_row[1]:
    st.write("")  # Right blank

st.markdown("<h3 style='text-align: center;'>Weather Fact Checking</h3>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-style: italic; font-size: 18px; margin-top: -10px; margin-bottom: 20px;'>Current Location: Mumbai</p>",
    unsafe_allow_html=True,
)

location = "Mumbai"
news_api = st.secrets.get("NEWSAPI_KEY", "YOUR_NEWSAPI_KEY")
weather_api = st.secrets.get("WEATHERAPI_KEY", "YOUR_OPENWEATHERMAP_KEY")

try:
    weather = get_live_weather(location, weather_api)
except Exception as e:
    st.error(f"Error fetching weather data: {e}")
    weather = None

if weather:
    st.markdown(
        f"<div style='text-align: center; font-size: 18px; margin-bottom: 40px;'>"
        f"<b>Temperature:</b> {weather['temp']}°C &nbsp;|&nbsp; "
        f"<b>Status:</b> {weather['status']} &nbsp;|&nbsp; "
        f"<i>{weather['desc'].capitalize()}</i></div>",
        unsafe_allow_html=True,
    )

try:
    news_list = get_latest_weather_news(location, news_api)
except Exception as e:
    st.error(f"Error fetching news: {e}")
    news_list = []

st.markdown("<h4 style='text-align: center;'>Latest Weather News</h4>", unsafe_allow_html=True)

# Display 3 news per row cleanly
for i in range(0, len(news_list), 3):
    news_cols = st.columns(3)
    for col_idx, news in enumerate(news_list[i : i + 3]):
        with news_cols[col_idx]:
            st.markdown(
                f"""<a href="{news['url']}" target="_blank" style="font-size:17px; font-weight:600; color:#222; text-decoration:none;">
                       {news['title']}</a><br>
                    <span style="color:#999; font-size:11px;">{news['source']} • {news['published']}</span><br>
                    <img src="{news['image']}" alt="news image" style="width:100%; margin: 8px 0; border-radius:6px;">
                    <p style="font-size:14px;">{news['description']}</p>""",
                unsafe_allow_html=True,
            )
            if weather:
                flag, prob, note = fact_check_claim(news["title"], weather)
                bar_color = "#4CAF50" if flag == "🟢" else "#FFC107" if flag == "🟡" else "#F44336"
                st.markdown(
                    f"""<b>Fact Check:</b> <span style="color:{bar_color}; font-weight:700;">{flag} {note}</span><br>
                    <div style="background:#ddd; border-radius:5px; height:12px; width:100%;">
                      <div style="width:{prob}%; background:{bar_color}; height:12px; border-radius:5px;"></div>
                    </div>""",
                    unsafe_allow_html=True,
                )


# Dropdown for each agent detailed explanation

with st.expander("How Each Agent Works - News Aggregator Agent"):
    st.markdown("""
    **Sources:**
    - NewsAPI.org: Weather news search endpoint querying "weather Mumbai"
    - Other news RSS feeds (optional)
    
    **Data fetched example format:**
    ```
    {
        "title": "Rain expected in Mumbai on Thursday",
        "url": "https://timesofindia.indiatimes.com/mumbai-weather-update",
        "image": "https://image-url.jpg",
        "source": "Times of India",
        "description": "IMD forecasts heavy rains in Mumbai; city on alert.",
        "published": "2025-08-28"
    }
    ```
    """)

with st.expander("How Each Agent Works - Weather Data Collector Agent"):
    st.markdown("""
    **Source:**
    - OpenWeatherMap API providing real-time weather data for location
    
    **Input:** City name string (e.g. "Mumbai")
    
    **Output example:**
    ```
    {
      "temp": 29.5,
      "status": "Rain",
      "desc": "light rain"
    }
    ```
    """)

with st.expander("How Each Agent Works - Fact Checking Agent"):
    st.markdown("""
    **Fact-checking Sources Used:**
    - Live weather data from OpenWeatherMap API
    - Aggregated news claims via NewsAPI
    
    **Fact-checking Logic:**
    - Extract weather-related keywords from news titles (e.g. rain, sunny, storm)
    - Compare keywords with live weather `status` field
    - Assign flag:
      - 🟢 Green if live weather supports claim
      - 🟡 Yellow if partially matches
      - 🔴 Red if contradicts
    
    **Example Input:**
    ```
    {
      "claim": "Rain expected in Mumbai on Thursday",
      "live_weather": {
          "temp": 29.5,
          "status": "Rain"
      }
    }
    ```
    
    **Example Output:**
    ```
    {
      "flag": "🟢",
      "probability": 91,
      "note": "Supported by live weather"
    }
    ```
    """)

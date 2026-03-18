import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import urllib.request
import xml.etree.ElementTree as ET
import utils

# Theming applies consistently to all pages via app.py routing
utils.apply_custom_styles()

# ---------------------------------------------
# 1. HELPER FUNCTIONS FOR REAL DATA
# ---------------------------------------------

@st.cache_data(ttl=3600)
def get_agri_news():
    """Fetches real-time agriculture news related to India/Uttarakhand using Google News RSS."""
    try:
        url = "https://news.google.com/rss/search?q=agriculture+uttarakhand+OR+farming+india&hl=en-IN&gl=IN&ceid=IN:en"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=5) as response:
            xml_data = response.read()
        root = ET.fromstring(xml_data)
        news_items = []
        for item in root.findall('.//item')[:3]:
            title = item.find('title').text
            link = item.find('link').text
            pubDate = item.find('pubDate').text
            news_items.append({"title": title, "link": link, "date": pubDate})
        return news_items
    except Exception as e:
        return []

@st.cache_data(ttl=1800)
def get_weather_data(lat, lon):
    """Fetches real-time weather using Open-Meteo free API."""
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&hourly=temperature_2m,relative_humidity_2m,precipitation&timezone=Asia/Kolkata"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        current = data.get("current_weather", {})
        hourly = data.get("hourly", {})
        daily = data.get("daily", {})
        
        # approximate humidity from hourly array
        time_str = current.get("time")
        idx = hourly.get("time", []).index(time_str) if time_str in hourly.get("time", []) else 0
        humidity = hourly.get("relative_humidity_2m", [])[idx] if hourly.get("relative_humidity_2m") else 50
        
        return {
            "current_temp": current.get("temperature", "--"),
            "wind": current.get("windspeed", "--"),
            "humidity": humidity,
            "daily_dates": daily.get("time", []),
            "daily_max": daily.get("temperature_2m_max", []),
            "daily_min": daily.get("temperature_2m_min", []),
            "daily_rain": daily.get("precipitation_sum", [])
        }
    except Exception as e:
        return None

# Locate major farming hubs in Uttarakhand + Delhi reference
LOCATIONS = {
    "Dehradun, Uttarakhand": (30.3165, 78.0322),
    "Nainital, Uttarakhand": (29.3919, 79.4542),
    "Almora, Uttarakhand": (29.5971, 79.6644),
    "Haridwar, Uttarakhand": (29.9457, 78.1642),
    "Pithoragarh, Uttarakhand": (29.5829, 80.2182),
    "Rishikesh, Uttarakhand": (30.0869, 78.2676),
    "New Delhi": (28.6139, 77.2090)
}

# ---------------------------------------------
# 2. HERO SECTION & LOCATION WRAPPER
# ---------------------------------------------
st.title(utils.get_text("dash"))
st.markdown(f"**{utils.get_text('dashboard_desc')}**")

st.markdown("---")

col_loc1, col_loc2 = st.columns([3, 1])
with col_loc2:
    selected_loc = st.selectbox("📍 Monitoring Location", list(LOCATIONS.keys()), index=0)

lat, lon = LOCATIONS[selected_loc]

# Fetch Real-time Data
with st.spinner("Fetching live environmental & agriculture data..."):
    weather_data = get_weather_data(lat, lon)
    news_data = get_agri_news()

# ---------------------------------------------
# 3. SMART SUMMARY CARDS
# ---------------------------------------------
st.markdown("### 🌾 Smart Summary")

# Yield prediction from session state
yield_pred = st.session_state.get("yield_pred")
if yield_pred:
    yp_text = f"{yield_pred:.2f} t/ha"
    yp_color = "#4CAF50" # Success Green
else:
    yp_text = "Pending"
    yp_color = "#9E9E9E" # Grey

# Evaluate Weather Risk dynamically if API succeeded
soil_status = utils.get_text("good")
weather_risk = utils.get_text("low")

if weather_data and weather_data["current_temp"] != "--":
    temp = weather_data["current_temp"]
    if temp > 40 or temp < 5:
        weather_risk = utils.get_text("high")
    elif 30 < temp <= 40:
        weather_risk = utils.get_text("moderate")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f'''
    <div class="metric-card" style="border-left-color: {yp_color};">
        <h3>📈 {utils.get_text("pred_yield")}</h3>
        <h2>{yp_text}</h2>
    </div>
    ''', unsafe_allow_html=True)
    
with col2:
    st.markdown(f'''
    <div class="metric-card" style="border-left-color: #8BC34A;">
        <h3>🌱 {utils.get_text("soil_health")}</h3>
        <h2>{soil_status}</h2>
    </div>
    ''', unsafe_allow_html=True)
    
with col3:
    risk_color = "#F44336" if "High" in weather_risk or "उच्च" in weather_risk else ("#FFA000" if "Moderate" in weather_risk or "मध्यम" in weather_risk else "#4CAF50")
    st.markdown(f'''
    <div class="metric-card" style="border-left-color: {risk_color};">
        <h3>🌦️ {utils.get_text("weather_risk")}</h3>
        <h2 style="color: {risk_color};">{weather_risk}</h2>
    </div>
    ''', unsafe_allow_html=True)
    
st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------
# 4. LIVE WEATHER PANEL & INSIGHTS CHART
# ---------------------------------------------
col_w, col_c = st.columns([1, 2])

with col_w:
    st.markdown(f"### 🌤 Live Weather")
    st.caption(f"Location: {selected_loc}")
    if weather_data:
        st.markdown(f'''
        <div class="metric-card" style="background: linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%); color: white; border-left:none; box-shadow: 0 8px 16px rgba(0,0,0,0.2);">
            <div style="font-size: 3rem; margin-bottom: -10px; font-weight: bold;">🌡️ {weather_data["current_temp"]}°C</div>
            <p style="font-size: 1.1rem; color: #E8F5E9; margin-top: 10px;">
                💧 Humidity: {weather_data["humidity"]}%<br>
                💨 Wind: {weather_data["wind"]} km/h
            </p>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.warning("Weather API unavailable at the moment. Please try again later.")

with col_c:
    st.markdown("### 📊 7-Day Weather & Rainfall Trend")
    if weather_data and weather_data.get("daily_dates"):
        df_forecast = pd.DataFrame({
            "Date": weather_data["daily_dates"],
            "Max Temp (°C)": weather_data["daily_max"],
            "Rain (mm)": weather_data["daily_rain"],
        })
        
        # Multi-axis plot for Temp and Rainfall overlap
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_forecast["Date"], 
            y=df_forecast["Rain (mm)"],
            name='Rainfall', 
            marker_color='#03A9F4', 
            yaxis='y2', 
            opacity=0.6
        ))
        fig.add_trace(go.Scatter(
            x=df_forecast["Date"], 
            y=df_forecast["Max Temp (°C)"],
            mode='lines+markers', 
            name='Max Temp', 
            line=dict(color='#FF5722', width=3)
        ))
        
        bg_color = "rgba(0,0,0,0)"
        is_dark = "Dark" in st.session_state.get("theme", "Light")
        font_color = "#E0E0E0" if is_dark else "#1C2819"
        
        fig.update_layout(
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
            font_color=font_color,
            xaxis=dict(showgrid=False),
            yaxis=dict(title="Temperature (°C)", showgrid=False),
            yaxis2=dict(title="Rainfall (mm)", overlaying='y', side='right', showgrid=False),
            margin=dict(t=10, l=10, r=10, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Chart data not available.")

st.markdown("---")

# ---------------------------------------------
# 5. AGRICULTURE NEWS SECTION
# ---------------------------------------------
st.markdown("### 📰 Latest Agriculture News & Updates")
if news_data:
    is_dark = "Dark" in st.session_state.get('theme', 'Light')
    card_bg = '#1E2A1E' if is_dark else '#F9FDF9'
    text_color = '#E0E0E0' if is_dark else '#333333'
    
    for news in news_data:
        st.markdown(f"""
        <div style="padding: 15px; border-radius: 8px; border: 1px solid #4CAF50; margin-bottom: 12px; background-color: {card_bg}; transition: transform 0.2s;">
            <h4 style="margin:0; margin-bottom: 5px;">
                <a href="{news['link']}" target="_blank" style="text-decoration: none; color: #4CAF50;">{news['title']}</a>
            </h4>
            <small style="color: {text_color}; opacity: 0.8;">📅 Published: {news['date']}</small>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Could not fetch the latest news at this moment. Please check back later.")

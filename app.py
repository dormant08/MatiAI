import streamlit as st
import utils

st.set_page_config(
    page_title="माटी AI - Smart Agriculture",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
utils.init_session_state()

# Apply CSS Theme 
utils.apply_custom_styles()

# Define Navigation
dashboard_page = st.Page("pages/dashboard.py", title=utils.get_text("dash"), icon="📊", default=True)
yield_page = st.Page("pages/yield_prediction.py", title=utils.get_text("yield_nav"), icon="📈")
soil_page = st.Page("pages/soil_health.py", title=utils.get_text("soil_nav"), icon="🌱")
weather_page = st.Page("pages/weather.py", title=utils.get_text("weather_nav"), icon="🌦️")
disease_page = st.Page("pages/disease_scanner.py", title=utils.get_text("disease_nav"), icon="🔍")
chat_page = st.Page("pages/chatbot.py", title=utils.get_text("chat_nav"), icon="🤖")

nav = st.navigation({
    utils.get_text("nav"): [dashboard_page, yield_page, soil_page, weather_page, disease_page, chat_page]
})

# Sidebar Configuration
st.sidebar.title(utils.get_text("title").split(":")[0])
st.sidebar.markdown(f"**{utils.get_text('tagline')}**")

st.sidebar.markdown("---")
st.sidebar.header(utils.get_text("settings"))

new_lang = st.sidebar.selectbox(
    utils.get_text("lang"), 
    ["English", "Hindi"], 
    index=0 if st.session_state.language == "English" else 1
)
if new_lang != st.session_state.language:
    st.session_state.language = new_lang
    st.rerun()

new_theme = st.sidebar.selectbox(
    utils.get_text("theme"), 
    ["Light ☀️", "Dark 🌙"], 
    index=0 if "Light" in st.session_state.theme else 1
)
if new_theme != st.session_state.theme:
    st.session_state.theme = new_theme
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("© 2024 माटी AI. Uttarakhand 🇮🇳")

# Run Page Navigation Router
nav.run()

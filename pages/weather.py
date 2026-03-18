import streamlit as st
import time
import utils

utils.apply_custom_styles()
st.title(utils.get_text("weather_title"))
    
st.info("Provides risk assessment based on localized weather conditions.")
w1, w2, w3 = st.columns(3)

with w1:
    temp_w = st.slider(utils.get_text("temp") + " ", -10, 50, 22)
with w2:
    hum_w = st.slider(utils.get_text("humidity") + " ", 0, 100, 55)
with w3:
    rain_w = st.slider(utils.get_text("rainfall") + " ", 0, 500, 20)
    
if st.button(utils.get_text("check_weather")):
    with st.spinner(utils.get_text("computing")):
        time.sleep(1)
        lang = st.session_state.get("language", "English")
        if temp_w > 40 or temp_w < 5 or rain_w > 300:
            risk = utils.get_text("high")
            alert = "Extreme weather alerts! Protect crops immediately." if lang == "English" else "चरम मौसम अलर्ट! तुरंत फसलों की रक्षा करें।"
            color = "red"
        elif 30 < temp_w <= 40 or hum_w > 80:
            risk = utils.get_text("moderate")
            alert = "Watch out for potential pest attacks due to high humidity." if lang == "English" else "उच्च आर्द्रता के कारण संभावित कीट हमलों से सावधान रहें।"
            color = "orange"
        else:
            risk = utils.get_text("low")
            alert = "Optimal conditions. Crop is safe." if lang == "English" else "इष्टतम स्थितियां। फसल सुरक्षित है।"
            color = "green"
            
        st.markdown(f"### {utils.get_text('risk_level')} <span style='color:{color}'>{risk}</span>", unsafe_allow_html=True)
        st.warning(f"**Alert:** {alert}")

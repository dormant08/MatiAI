import streamlit as st
import time
import utils

utils.apply_custom_styles()
st.title(utils.get_text("soil_title"))
    
c1, c2 = st.columns(2)
with c1:
    ph = st.slider(utils.get_text("ph"), 0.0, 14.0, 6.5)
    moist = st.slider(utils.get_text("moisture"), 0, 100, 40)
with c2:
    n = st.number_input(utils.get_text("nitrogen"), 0, 200, 50)
    p = st.number_input(utils.get_text("phosphorus"), 0, 100, 20)
    k = st.number_input(utils.get_text("potassium"), 0, 100, 30)
    
if st.button(utils.get_text("analyze_btn")):
    with st.spinner(utils.get_text("computing")):
        time.sleep(1)
        lang = st.session_state.get("language", "English")
        
        if 6.0 <= ph <= 7.5 and n > 40 and moist > 30:
            qual = utils.get_text("good")
            sug = "Soil is well balanced. Continue current practices." if lang == "English" else "मिट्टी अच्छी तरह से संतुलित है। वर्तमान प्रथाओं को जारी रखें।"
            color = "green"
        elif ph < 5.5 or ph > 8.0 or n < 20:
            qual = utils.get_text("poor")
            sug = "Add lime if pH is low. Use NPK fertilizers. Improve irrigation." if lang == "English" else "यदि पीएच कम है तो चूना डालें। एनपीके उर्वरकों का प्रयोग करें। सिंचाई में सुधार करें।"
            color = "red"
        else:
            qual = utils.get_text("moderate")
            sug = "Consider adding organic compost to boost nutrients." if lang == "English" else "पोषक तत्वों को बढ़ावा देने के लिए जैविक खाद जोड़ने पर विचार करें।"
            color = "orange"
            
        st.markdown(f"### {utils.get_text('soil_quality')} <span style='color:{color}'>{qual}</span>", unsafe_allow_html=True)
        st.info(f"**{utils.get_text('suggestion')}** {sug}")

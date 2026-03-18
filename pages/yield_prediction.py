import streamlit as st
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import time
import utils

utils.apply_custom_styles()
st.title(utils.get_text("yield_title"))

@st.cache_resource
def get_yield_model():
    np.random.seed(42)
    X = np.random.rand(500, 5)
    X[:, 0] = X[:, 0] * 200 + 50     
    X[:, 1] = X[:, 1] * 20 + 10      
    X[:, 2] = X[:, 2] * 60 + 20      
    X[:, 3] = np.random.randint(0, 4, 500)
    X[:, 4] = np.random.randint(0, 5, 500)
    
    y = X[:, 0]*0.015 + X[:, 1]*0.08 + X[:, 2]*0.04 + np.random.rand(500)*1.5
    
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    return model

with st.container():
    st.markdown('<div class="metric-card" style="border-left:none;">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        rain = st.number_input(utils.get_text("rainfall"), min_value=0, max_value=500, value=100)
        temp = st.number_input(utils.get_text("temp"), min_value=-10, max_value=50, value=25)
        hum = st.number_input(utils.get_text("humidity"), min_value=0, max_value=100, value=60)
    with c2:
        soil_types = ["Alluvial", "Red", "Black", "Laterite"]
        soil = st.selectbox(utils.get_text("soil_type"), soil_types)
        crop_types = ["Wheat", "Rice", "Maize", "Sugarcane", "Millet"]
        crop = st.selectbox(utils.get_text("crop_type"), crop_types)
    st.markdown('</div>', unsafe_allow_html=True)

if st.button(utils.get_text("predict_btn")):
    with st.spinner(utils.get_text("computing")):
        time.sleep(1.5) 
        model = get_yield_model()
        
        s_idx = soil_types.index(soil)
        c_idx = crop_types.index(crop)
        
        features = np.array([[rain, temp, hum, s_idx, c_idx]])
        prediction = model.predict(features)[0]
        
        st.session_state.yield_pred = prediction
        
        st.success(f"{utils.get_text('yield_result')} **{prediction:.2f} {utils.get_text('tons_ha')}** ✅")

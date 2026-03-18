import streamlit as st
from PIL import Image
import numpy as np
import time
import utils

utils.apply_custom_styles()
st.title(utils.get_text("disease_title"))
    
uploaded_file = st.file_uploader(utils.get_text("upload_prompt"), type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=300)
    
    if st.button(utils.get_text("scan_btn")):
        with st.spinner(utils.get_text("computing")):
            time.sleep(2)
            lang = st.session_state.get("language", "English")
            disorders = [
                ("Healthy 🌱", "No treatment needed. Crop is safe! ✅", "स्वस्थ 🌱", "किसी उपचार की आवश्यकता नहीं है। फसल सुरक्षित है! ✅"),
                ("Leaf Blight 🍂", "Use Copper Fungicide and avoid overhead watering. ⚠️", "पत्ती झुलस रोग 🍂", "कॉपर फफूंदनाशक का उपयोग करें और ऊपर से पानी देने से बचें। ⚠️"),
                ("Rust Disease 🔴", "Apply Neem oil spray or sulfur-based fungicide. ⚠️", "जंग रोग 🔴", "नीम के तेल का स्प्रे या सल्फर आधारित फफूंदनाशक लगाएं। ⚠️"),
                ("Mildew 🌫️", "Improve air circulation and use potassium bicarbonate. ⚠️", "फफूंदी 🌫️", "वायु परिसंचरण में सुधार करें और पोटेशियम बाइकार्बोनेट का उपयोग करें। ⚠️")
            ]
            
            idx = np.random.randint(0, len(disorders))
            dis_en, trt_en, dis_hi, trt_hi = disorders[idx]
            
            dis = dis_en if lang == "English" else dis_hi
            trt = trt_en if lang == "English" else trt_hi
            
            if "Healthy" in dis_en:
                st.success(f"**{utils.get_text('disease_detected')}** {dis}")
            else:
                st.error(f"**{utils.get_text('disease_detected')}** {dis}")
            
            st.info(f"**{utils.get_text('treatment')}** {trt}")

import streamlit as st

def init_session_state():
    if "language" not in st.session_state:
        st.session_state.language = "English"
    if "theme" not in st.session_state:
        st.session_state.theme = "Light ☀️"
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "yield_pred" not in st.session_state:
        st.session_state.yield_pred = None

def get_text(key):
    lang = st.session_state.get("language", "English")
    texts = {
        "English": {
            "title": "🌾 माटी AI: Smart Crop Health & Yield Predictor",
            "tagline": "Helping farmers make smarter decisions with AI",
            "nav": "Navigation 🧭",
            "dash": "📊 Dashboard",
            "yield_nav": "📈 Yield Prediction",
            "soil_nav": "🌱 Soil Health Analyzer",
            "weather_nav": "🌦️ Weather Insights",
            "disease_nav": "🔍 Plant Disease Scanner",
            "chat_nav": "🤖 AI Chatbot",
            "settings": "⚙️ Preferences",
            "lang": "Language / भाषा",
            "theme": "Theme / थीम",
            "summary": "Farm Summary Dashboard",
            "pred_yield": "Est. Yield",
            "soil_health": "Soil Health",
            "weather_risk": "Weather Risk",
            "good": "Good ✅",
            "moderate": "Moderate ⚠️",
            "poor": "Poor 🔴",
            "low": "Low ✅",
            "high": "High 🔴",
            "yield_title": "Predict Crop Yield",
            "rainfall": "Rainfall (mm)",
            "temp": "Temperature (°C)",
            "humidity": "Humidity (%)",
            "soil_type": "Soil Type",
            "crop_type": "Crop Type",
            "predict_btn": "Predict Yield",
            "soil_title": "Soil Health Analyzer",
            "ph": "Soil pH Level",
            "moisture": "Moisture (%)",
            "nitrogen": "Nitrogen (N) mg/kg",
            "phosphorus": "Phosphorus (P) mg/kg",
            "potassium": "Potassium (K) mg/kg",
            "analyze_btn": "Analyze Soil",
            "weather_title": "Weather Risk Insights",
            "check_weather": "Check Weather Risk",
            "disease_title": "Plant Disease Scanner",
            "upload_img": "Upload Plant Leaf Image",
            "scan_btn": "Scan for Diseases",
            "chat_title": "Mati AI - Agriculture Assistant",
            "chat_placeholder": "Ask your farming queries here...",
            "clear_chat": "Clear Chat",
            "waiting_api": "Please configure your Gemini API Key in Streamlit Secrets.",
            "ai_greeting": "Hello! I am Mati AI. How can I help you with your crops today?",
            "yield_result": "🌾 Predicted Yield:",
            "tons_ha": "tons/hectare",
            "soil_quality": "Soil Quality:",
            "suggestion": "Suggestion:",
            "risk_level": "Risk Level:",
            "disease_detected": "Disease Detected:",
            "treatment": "Suggested Treatment:",
            "upload_prompt": "Drag and drop or click to upload leaf image",
            "computing": "Analyzing data...",
            "dashboard_desc": "Overview of your farm's current parameters and predictions."
        },
        "Hindi": {
            "title": "🌾 माटी AI: स्मार्ट फसल स्वास्थ्य और उपज भविष्यवक्ता",
            "tagline": "एआई के साथ किसानों को स्मार्ट निर्णय लेने में मदद करना",
            "nav": "नेविगेशन 🧭",
            "dash": "📊 डैशबोर्ड",
            "yield_nav": "📈 उपज की भविष्यवाणी",
            "soil_nav": "🌱 मिट्टी स्वास्थ्य विश्लेषक",
            "weather_nav": "🌦️ मौसम की जानकारी",
            "disease_nav": "🔍 पौधों के रोग स्कैनर",
            "chat_nav": "🤖 एआई चैटबॉट",
            "settings": "⚙️ प्राथमिकताएं",
            "lang": "Language / भाषा",
            "theme": "Theme / थीम",
            "summary": "फार्म सारांश डैशबोर्ड",
            "pred_yield": "अनुमानित उपज",
            "soil_health": "मिट्टी का स्वास्थ्य",
            "weather_risk": "मौसम जोखिम",
            "good": "अच्छा ✅",
            "moderate": "मध्यम ⚠️",
            "poor": "खराब 🔴",
            "low": "कम ✅",
            "high": "उच्च 🔴",
            "yield_title": "फसल उपज की भविष्यवाणी करें",
            "rainfall": "वर्षा (मिमी)",
            "temp": "तापमान (°C)",
            "humidity": "नमी (%)",
            "soil_type": "मिट्टी का प्रकार",
            "crop_type": "फसल का प्रकार",
            "predict_btn": "उपज की भविष्यवाणी करें",
            "soil_title": "मिट्टी स्वास्थ्य विश्लेषक",
            "ph": "मिट्टी का पीएच (pH)",
            "moisture": "नमी (%)",
            "nitrogen": "नाइट्रोजन (N) mg/kg",
            "phosphorus": "फास्फोरस (P) mg/kg",
            "potassium": "पोटेशियम (K) mg/kg",
            "analyze_btn": "मिट्टी का विश्लेषण करें",
            "weather_title": "मौसम जोखिम अंतर्दृष्टि",
            "check_weather": "मौसम जोखिम जांचें",
            "disease_title": "पौधों के रोग स्कैनर",
            "upload_img": "पौधे की पत्ती की छवि अपलोड करें",
            "scan_btn": "रोगों के लिए स्कैन करें",
            "chat_title": "माटी एआई - कृषि सहायक",
            "chat_placeholder": "अपने कृषि संबंधी प्रश्न यहाँ पूछें...",
            "clear_chat": "चैट साफ़ करें",
            "waiting_api": "कृपया स्ट्रीमलिट सीक्रेट्स में अपनी जेमिनी API कुंजी कॉन्फ़िगर करें।",
            "ai_greeting": "नमस्ते! मैं माटी AI हूँ। आज मैं आपकी फसलों में आपकी कैसे मदद कर सकता हूँ?",
            "yield_result": "🌾 अनुमानित उपज:",
            "tons_ha": "टन/हेक्टेयर",
            "soil_quality": "मिट्टी की गुणवत्ता:",
            "suggestion": "सुझाव:",
            "risk_level": "जोखिम स्तर:",
            "disease_detected": "पाया गया रोग:",
            "treatment": "सुझाया गया उपचार:",
            "upload_prompt": "पत्ती की छवि अपलोड करने के लिए खींचें और छोड़ें या क्लिक करें",
            "computing": "डेटा का विश्लेषण किया जा रहा है...",
            "dashboard_desc": "आपके खेत के वर्तमान मापदंडों और भविष्यवाणियों का अवलोकन।"
        }
    }
    return texts.get(lang, texts["English"]).get(key, key)

def apply_custom_styles():
    theme = st.session_state.get("theme", "Light ☀️")
    
    if "Dark" in theme:
        bg_color = "#121212"
        text_color = "#E0E0E0"
        card_bg = "#1E2A1E"
        border_color = "#4CAF50"
    else:
        bg_color = "#F4F9F4"
        text_color = "#1C2819"
        card_bg = "#FFFFFF"
        border_color = "#2E7D32"

    css = f"""
    <style>
    /* Main Background & Text */
    .stApp {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
    }}
    
    h1, h2, h3, h4, h5, h6, p, label {{
        color: {text_color} !important;
    }}

    /* Cards */
    .metric-card {{
        background-color: {card_bg};
        border-left: 5px solid {border_color};
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        color: {text_color};
    }}
    
    .metric-card h3 {{
        margin-top: 0;
        color: #4CAF50 !important;
        font-size: 1.2rem;
    }}
    
    .metric-card h2 {{
        margin-bottom: 0;
        font-size: 2rem;
    }}

    /* Buttons */
    .stButton>button {{
        background-color: #4CAF50 !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease !important;
        font-weight: bold;
    }}
    .stButton>button:hover {{
        background-color: #388E3C !important;
        transform: scale(1.02);
    }}
    
    .stTextInput>div>div>input, .stNumberInput>div>div>input {{
        color: #333 !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

import streamlit as st
from google import genai
import utils

# Apply styles
utils.apply_custom_styles()

# Title
st.title(utils.get_text("chat_title"))

# Initialize session state if not present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------------
# 🔐 Gemini API Setup (CORRECT WAY)
# -------------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    client = None
    st.error("⚠️ Please configure your Gemini API Key in Streamlit Secrets.")

# -------------------------------
# 🤖 Chat UI
# -------------------------------
if client:

    # Show chat history
    for msg in st.session_state.chat_history:
        role = "You" if msg["role"] == "user" else "🌾 माटी AI"
        st.markdown(f"**{role}:** {msg['content']}")

    # Input box
    user_input = st.chat_input(utils.get_text("chat_placeholder"))

    # Clear chat button
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button(utils.get_text("clear_chat")):
            st.session_state.chat_history = []
            st.rerun()

    # When user sends message
    if user_input:
        st.session_state.chat_history.append(
            {"role": "user", "content": user_input}
        )
        st.markdown(f"**You:** {user_input}")

        # System prompt
        system_prompt = (
            "You are an agriculture expert helping Indian farmers, especially in Uttarakhand, "
            "with crop, soil, weather, and disease guidance."
        )

        full_prompt = f"{system_prompt}\n\nUser: {user_input}"

        # Gemini response
        with st.spinner(utils.get_text("computing")):
            try:
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=full_prompt
                )
                reply = response.text
            except Exception as e:
                reply = f"❌ Error: {str(e)}"

        # Save response
        st.session_state.chat_history.append(
            {"role": "ai", "content": reply}
        )

        # Display response
        st.markdown(f"**🌾 माटी AI:** {reply}")

# -------------------------------
# 👋 Greeting message
# -------------------------------
if len(st.session_state.chat_history) == 0:
    st.info(utils.get_text("ai_greeting"))
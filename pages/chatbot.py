import streamlit as st
import google.generativeai as genai
import utils

# Apply styles
utils.apply_custom_styles()

# Title
st.title(utils.get_text("chat_title"))

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------------
# 🔐 Gemini API Setup (CORRECT & STABLE)
# -------------------------------
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-pro")
except Exception:
    model = None
    st.error("⚠️ Please configure your Gemini API Key in Streamlit Secrets.")

# -------------------------------
# 🤖 Chat UI
# -------------------------------
if model:

    # Show chat history
    for msg in st.session_state.chat_history:
        role = "You" if msg["role"] == "user" else "🌾 माटी AI"
        st.markdown(f"**{role}:** {msg['content']}")

    # Chat input
    user_input = st.chat_input(utils.get_text("chat_placeholder"))

    # Clear chat button
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button(utils.get_text("clear_chat")):
            st.session_state.chat_history = []
            st.rerun()

    # Handle user input
    if user_input:
        st.session_state.chat_history.append(
            {"role": "user", "content": user_input}
        )
        st.markdown(f"**You:** {user_input}")

        # System prompt
        system_prompt = (
            "You are an agriculture expert helping Indian farmers, especially in Uttarakhand, "
            "with crop, soil, weather, and disease guidance. "
            "Give simple, practical, and easy-to-understand advice."
        )

        full_prompt = f"{system_prompt}\n\nUser: {user_input}"

        # Generate response
        with st.spinner(utils.get_text("computing")):
            try:
                response = model.generate_content(full_prompt)
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
import streamlit as st
from google import genai

# Initialize Gemini client
def get_gemini_client():
    api_key = st.secrets["GEMINI_API_KEY"]
    return genai.Client(api_key=api_key)

# Convert chat history to plain text
def format_history(history, user_message):
    text = ""
    for msg in history:
        speaker = "User" if msg["role"] == "user" else "Assistant"
        text += f"{speaker}: {msg['content']}\n"
    text += f"User: {user_message}\nAssistant:"
    return text

# Generate response
def get_chatbot_reply(prompt, history):
    try:
        client = get_gemini_client()

        formatted = format_history(history, prompt)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=formatted      # <-- Gemini accepts plain string here
        )

        return response.text

    except Exception as e:
        return f"Error: {e}"

# Streamlit App
def main():
    st.title("🤖 AI Chatbot")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.chat_input("Say something...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        bot_reply = get_chatbot_reply(user_input, st.session_state.chat_history)

        st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

    # Display chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

if __name__ == "__main__":
    main()

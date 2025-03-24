import streamlit as st
import requests  # To send HTTP requests to your backend API

# App Title and Layout
st.set_page_config(page_title="AgentX - Your AI Assistant", layout="wide")
st.title("🤖 AgentX - AI Chatbot")

# Initialize message history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous chat messages
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message to chat history
    st.session_state["messages"].append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):  # Show loading indicator
            try:
                # API Endpoint of the Flask backend (replace with your actual API URL)
                api_url = "http://<your-public-ip>:5000/chat"  # Replace with your actual public IP/hostname

                # Send the message to the Flask API
                response = requests.post(
                    api_url, json={"message": user_input}
                )

                # Check if the request was successful
                if response.status_code == 200:
                    # Extract the response from the API
                    reply = response.json().get("response", "Sorry, I couldn't get a response.")
                else:
                    reply = f"⚠️ Error: Unable to generate response. Status Code: {response.status_code}"

            except Exception as e:
                # Handle errors during the API call
                reply = f"⚠️ Error: Unable to generate response. Details: {e}"

        # Display the AI response
        st.markdown(reply)

    # Add AI response to chat history
    st.session_state["messages"].append({"role": "assistant", "content": reply})

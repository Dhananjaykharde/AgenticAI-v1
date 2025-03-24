import streamlit as st
import ollama

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
                # Get response from ollama API
                response = ollama.chat(model="llama3:latest", messages=st.session_state["messages"])

                # Debugging: Print the entire response object to check its structure
                st.write(response)  # Remove this line once you identify the structure

                # Check if the response contains the expected structure
                if "message" in response and "content" in response["message"]:
                    reply = response["message"]["content"]
                else:
                    reply = "⚠️ Error: Unexpected response structure. Please try again later."
            
            except Exception as e:
                # Catch and display any errors in the response
                reply = f"⚠️ Error: Unable to generate response. Details: {e}"

        st.markdown(reply)

    # Add AI response to chat history
    st.session_state["messages"].append({"role": "assistant", "content": reply})

# DSC 670 Project
# PERSONAL FINANCE CHATBOT
# Christopher Stemm
# Bellevue University
# DSC 670 - Advanced uses of Generative AI

# Thanks to Tattooed Chef for code snippits for streamlit aesthetics.

import streamlit as st
from openai import OpenAI

client = OpenAI()


def generate_response(prompt, temperature=0.2, max_tokens=256, top_p=0.9, n=2, stop=None, frequency_penalty=0.5,
                      presence_penalty=0.5, chat_history=None):
    if chat_history is None:
        chat_history = []

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]
    messages.extend(chat_history)

    response = client.chat.completions.create(
        model="ft:gpt-4o-mini-2024-07-18:personal:finance:Az8PLsfl",
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        n=n,
        stop=stop,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )

    return response.choices[0].message.content


st.set_page_config(page_title="Personal Fiance Chatbot | By Chris Stemm @ Bellevue University", layout="wide")
st.write("# Milo the Personal Finance Chatbot :moneybag: ")
st.write("Hello, I'm Milo the finance chatbot! Type your message below:")

# HTML sidebar to adjust model's parameters.
st.sidebar.markdown("# Model Parameters")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
max_tokens = st.sidebar.number_input("Max Tokens", 50, 500, 256, step=50)
top_p = st.sidebar.slider("Top P", 0.1, 1.0, 0.9, 0.1)
n = st.sidebar.number_input("N", 1, 5, 2, step=1)
stop = st.sidebar.text_input("Stop", "")
frequency_penalty = st.sidebar.slider("Frequency Penalty", 0.0, 1.0, 0.9, 0.1)
presence_penalty = st.sidebar.slider("Presence Penalty", 0.0, 1.0, 0.9, 0.1)

# User enters prompt and gets the response.
user_input = st.text_area("You:", "", key="user_input")
generate_button = st.button("Generate Response")

# Chat history.
messages = []
if user_input.strip() != "":
    messages.append({"role": "user", "content": user_input})
    response = generate_response(user_input, temperature, max_tokens, top_p, n, stop, frequency_penalty,
                                 presence_penalty)
    messages.append({"role": "assistant", "content": response})

st.subheader("Chat History")
for message in messages:
    if message["role"] == "user":
        st.text_area("You:", value=message["content"], height=80, max_chars=200, key="user_history", disabled=True)
    else:
        st.text_area("Milo:", value=message["content"], height=500, key="chatbot_history")

# Additional styling for aesthetics.
st.markdown(
    """
    <style>
        body {
            font-family: Montserrat, sans-serif;
        }
        .stTextInput>div>div>textarea {
            background-color: #f0f0f0;
            color: #000;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        .stTextArea>div>textarea {
            resize: none;
        }
        .st-subheader {
            margin-top: 20px;
            font-size: 16px;
        }
        .stTextArea>div>div>textarea {
            height: 100px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

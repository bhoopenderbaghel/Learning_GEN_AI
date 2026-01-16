from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

st.header("Research Tool")

user_input = st.text_input("Enter Your Prompt")
model = ChatOpenAI(model = "gpt-4o-mini")
if st.button('Summarize'):
    result = model.invoke(user_input)
    st.write(result.content)



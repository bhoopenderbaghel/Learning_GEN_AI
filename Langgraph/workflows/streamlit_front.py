import streamlit as st
from chatbot_langgraph import chatbot
from langchain.messages import HumanMessage
import uuid

# Utility function #####
def generate_thread_id():
    thread_id = uuid.uuid4()
    
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

CONFIG = {'configurable':{'thread_id': 'thread-1'}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

add_thread(st.session_state['thread_id'])

st.sidebar.title("Langgraph ChatBot")

if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("My Conversations")

st.sidebar.text(st.session_state['thread_id'])

# Loading the converstion history
for message in st.session_state['message_history'] :
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type here')

if user_input:

    st.session_state['message_history'] .append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)
    # try:

        # response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]},config=CONFIG)
        # ai_message = response['messages'][-1].content
    # except Exception as e:
    #     st.error(str(e))
    #     st.stop()
     # st.session_state['message_history'] .append({'role':'assistant', 'content': ai_message})
    
    with st.chat_message('assistant'):
        # st.text(ai_message)
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
            {'messages': [HumanMessage(content= user_input)]},
            config= CONFIG,
            stream_mode= 'messages'
        )
        )
    st.session_state['message_history'] .append({'role':'assistant', 'content': ai_message})  
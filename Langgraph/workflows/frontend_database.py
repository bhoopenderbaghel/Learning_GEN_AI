import streamlit as st
from langgraph_database_backend import chatbot,retrieve_all_thread
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

def load_converstion(thread_id):
    return chatbot.get_state(config={'configurable':{'thread_id': thread_id}}).values.get("messages",[])


if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_thread()

add_thread(st.session_state['thread_id'])

st.sidebar.title("Langgraph ChatBot")

if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("My Conversations")
for  thread_id in st.session_state['chat_threads']:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_converstion(thread_id)

        temp_messages = []

        for message in messages:
            if isinstance(message,HumanMessage):
                role = "user"
            else:
                role = "assistant"

            temp_messages.append({'role': role, 'content': message.content})
        st.session_state["message_history"]  = temp_messages


# Loading the converstion history
for message in st.session_state['message_history'] :
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type here')

if user_input:

    st.session_state['message_history'] .append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    CONFIG = {
        'configurable': {
            'thread_id': st.session_state['thread_id']
        },
        "metadata":{"thread_id": st.session_state['thread_id']},
        "run_name": "chat_node",
    }
        
    with st.chat_message('assistant'):
        # st.text(ai_message)
        ai_message = st.write_stream(
        (message_chunk.content for message_chunk, metadata in chatbot.stream(
        {'messages': [HumanMessage(content=user_input)]},
        # config={'configurable': {'thread_id': st.session_state['thread_id']}},
        config = CONFIG,
        stream_mode='messages'
    ))
        )
    st.session_state['message_history'] .append({'role':'assistant', 'content': ai_message})  